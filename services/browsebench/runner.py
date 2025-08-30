# services/browsebench/runner.py
import asyncio
import os
import json
from openai import OpenAI
from playwright.async_api import async_playwright
from .config.models import ModelConfig
from .metrics import MetricsCollector, BenchmarkResults, TestResult
from .test_suite import TestSuite, Test
from .agent_tools import BrowserAgentTools
from .openai_tools import get_tool_definitions

class BrowseBenchRunner:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.model = self._setup_model(model_config)
        self.metrics = MetricsCollector()
        self.playwright = None
        self.browser = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def _setup_model(self, model_config: ModelConfig):
        api_key = model_config.api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Set it in model_configs.json or as an environment variable.")
        
        base_url = model_config.base_url or "https://openrouter.ai/api/v1"

        return OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    async def _execute_test(self, test: Test) -> TestResult:
        page = await self.browser.new_page()
        tools = BrowserAgentTools(page)
        tool_definitions = get_tool_definitions(tools)

        system_prompt = """
        You are a web browsing agent. You will be given a task and a set of tools to interact with a web page.
        Your goal is to complete the task by using the tools.
        You can use the following tools:
        - navigate(url: str): Navigates to a given URL.
        - click(selector: str): Clicks on an element specified by a CSS selector.
        - type_text(selector: str, text: str): Types text into an input field.
        - get_text(selector: str): Gets the text content of an element.
        - get_html(selector: str = 'body'): Gets the HTML content of an element.
        - finish(result: str): Call this function when you have completed the task.
        
        You will be given the initial HTML of the page. Then, you will receive the output of your tool calls.
        Think step-by-step and use the tools to achieve the goal.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"The task is: {test.goal}. The starting URL is: {test.url}"}
        ]

        await tools.navigate(test.url)
        
        start_time = asyncio.get_event_loop().time()
        steps = 0
        total_tokens = 0
        total_cost = 0

        for _ in range(10): # Max 10 steps
            steps += 1
            html = await tools.get_html()
            messages.append({"role": "user", "content": f"""Current page HTML:
{html}"""})

            response = self.model.chat.completions.create(
                model=self.model_config.model,
                messages=messages,
                tools=tool_definitions,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            total_tokens += response.usage.total_tokens
            total_cost += response.usage.cost

            if not response_message.tool_calls:
                break

            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            
            if function_name == "finish":
                function_args = json.loads(tool_call.function.arguments)
                await page.close()
                return TestResult(
                    test_name=test.name,
                    success=True,
                    steps=steps,
                    response_time=asyncio.get_event_loop().time() - start_time,
                    token_usage=total_tokens,
                    cost=total_cost,
                    details={"finish_reason": function_args.get("result")}
                )

            available_tools = {t['function']['name']: getattr(tools, t['function']['name']) for t in tool_definitions}
            tool_function = available_tools.get(function_name)
            
            if tool_function:
                function_args = json.loads(tool_call.function.arguments)
                try:
                    result = await tool_function(**function_args)
                    messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": function_name, "content": str(result)})
                except Exception as e:
                    messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": function_name, "content": f"Error: {e}"})
            else:
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": function_name, "content": "Error: Tool not found."})

        await page.close()
        
        return TestResult(
            test_name=test.name,
            success=False,
            steps=steps,
            response_time=asyncio.get_event_loop().time() - start_time,
            token_usage=total_tokens,
            cost=total_cost,
            details={"finish_reason": "Max steps reached."}
        )

    async def run_benchmark(self, test_suite: TestSuite) -> BenchmarkResults:
        for test in test_suite:
            result = await self._execute_test(test)
            self.metrics.add_result(result)
        
        return self.metrics.aggregate_results()

if __name__ == '__main__':
    import argparse
    import asyncio
    from .config.models import MODEL_CONFIGS, ModelConfig
    from .test_suite import load_test_from_yaml

    parser = argparse.ArgumentParser(description="BrowseBench Benchmark Runner")
    parser.add_argument("--models", nargs='+', default=["google/gemini-flash-1.5"], help="Models to use for the benchmark")
    parser.add_argument("--test_dir", type=str, default="services/browsebench/tests", help="Directory containing test YAML files")
    parser.add_argument("--test_file", type=str, default=None, help="Path to a single test YAML file to run.")
    args = parser.parse_args()

    async def run_single_benchmark(model_name, test_suite):
        if model_name not in MODEL_CONFIGS:
            raise ValueError(f"Model {model_name} not found in configuration.")
        
        model_config_data = MODEL_CONFIGS[model_name]
        model_config = ModelConfig(**model_config_data)
        
        print(f"Running benchmark for model: {model_name}")
        async with BrowseBenchRunner(model_config=model_config) as runner:
            results = await runner.run_benchmark(test_suite)
            return {model_name: results.dict()}

    async def main():
        if args.test_file:
            test_suite = [load_test_from_yaml(args.test_file)]
        else:
            test_files = [os.path.join(args.test_dir, f) for f in os.listdir(args.test_dir) if f.endswith('.yaml')]
            test_suite = [load_test_from_yaml(f) for f in test_files]

        tasks = [run_single_benchmark(model_name, test_suite) for model_name in args.models]
        all_results = await asyncio.gather(*tasks)
        
        final_results = {}
        for res in all_results:
            final_results.update(res)
            
        os.makedirs("results", exist_ok=True)
        with open("results/benchmark_results.json", "w") as f:
            json.dump(final_results, f, indent=4)
            
        print("Benchmark finished. Results saved to results/benchmark_results.json")

    asyncio.run(main())