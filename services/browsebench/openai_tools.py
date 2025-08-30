import inspect
import json
from .agent_tools import BrowserAgentTools

def get_tool_definitions(tools: BrowserAgentTools):
    tool_definitions = []
    for name, method in inspect.getmembers(tools, predicate=inspect.iscoroutinefunction):
        if name.startswith("__"):
            continue

        sig = inspect.signature(method)
        docstring = inspect.getdoc(method)
        description = ""
        if docstring:
            description = docstring.split('\n')[0]

        parameters = {
            "type": "object",
            "properties": {},
            "required": [],
        }

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            
            param_type = "string"
            if param.annotation == int:
                param_type = "integer"
            elif param.annotation == float:
                param_type = "number"
            elif param.annotation == bool:
                param_type = "boolean"

            parameters["properties"][param_name] = {
                "type": param_type,
                "description": "",
            }
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(param_name)

        tool_definitions.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            }
        )
    tool_definitions.append(
        {
            "type": "function",
            "function": {
                "name": "finish",
                "description": "Call this function when you have completed the task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "string", "description": "The result of the task."}
                    },
                    "required": ["result"],
                },
            },
        },
    )
    return tool_definitions

