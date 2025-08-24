# services/browsebench/runner.py
import asyncio
from playwright.async_api import async_playwright
from .config.models import ModelConfig
from .metrics import MetricsCollector, BenchmarkResults, TestResult
from .test_suite import TestSuite, Test
from .agent_tools import BrowserAgentTools

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
        # Placeholder for OpenRouter integration
        print(f"Setting up model: {model_config.model}")
        return None

    async def _execute_test(self, test: Test) -> TestResult:
        page = await self.browser.new_page()
        tools = BrowserAgentTools(page)

        print(f"Executing test: {test.name}")

        # Simulate agent interaction
        await tools.navigate(test.url)
        await tools.type_text("#search", "AI agent")
        await tools.click("#search-button")
        content = await tools.get_html()

        await page.close()

        # Placeholder for result calculation
        return TestResult(
            test_name=test.name,
            success=True,
            steps=3, # navigate, type, click
            response_time=2.5,
            token_usage=200,
            cost=0.02,
        )

    async def run_benchmark(self, test_suite: TestSuite) -> BenchmarkResults:
        for test in test_suite:
            result = await self._execute_test(test)
            self.metrics.add_result(result)
        
        return self.metrics.aggregate_results()

if __name__ == '__main__':
    import argparse
    import os
    import asyncio
    from .config.models import MODEL_CONFIGS, ModelConfig
    from .test_suite import load_test_from_yaml

    parser = argparse.ArgumentParser(description="BrowseBench Benchmark Runner")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model to use for the benchmark")
    parser.add_argument("--test_dir", type=str, default="services/browsebench/tests", help="Directory containing test YAML files")
    args = parser.parse_args()

    if args.model not in MODEL_CONFIGS:
        raise ValueError(f"Model {args.model} not found in configuration.")

    model_config_data = MODEL_CONFIGS[args.model]
    model_config = ModelConfig(**model_config_data)

    test_files = [os.path.join(args.test_dir, f) for f in os.listdir(args.test_dir) if f.endswith('.yaml')]
    test_suite = [load_test_from_yaml(f) for f in test_files]

    async def main():
        async with BrowseBenchRunner(model_config=model_config) as runner:
            results = await runner.run_benchmark(test_suite)
            print(results)

    asyncio.run(main())