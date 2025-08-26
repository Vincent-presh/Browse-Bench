# services/browsebench/openai_tools.py

def get_tool_definitions():
    return [
        {
            "type": "function",
            "function": {
                "name": "navigate",
                "description": "Navigates to a given URL.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "The URL to navigate to."}
                    },
                    "required": ["url"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "click",
                "description": "Clicks on an element specified by a CSS selector.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "The CSS selector of the element to click."}
                    },
                    "required": ["selector"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "type_text",
                "description": "Types text into an input field.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "The CSS selector of the input field."},
                        "text": {"type": "string", "description": "The text to type."}
                    },
                    "required": ["selector", "text"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_text",
                "description": "Gets the text content of an element.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "The CSS selector of the element."}
                    },
                    "required": ["selector"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_html",
                "description": "Gets the HTML content of an element.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "selector": {"type": "string", "description": "The CSS selector of the element. Defaults to 'body'."}
                    },
                },
            },
        },
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
    ]
