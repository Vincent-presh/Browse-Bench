from dataclasses import dataclass

@dataclass
class ModelConfig:
    provider: str
    model: str
    max_tokens: int

MODEL_CONFIGS = {
    "gpt-4": {
        "provider": "openai",
        "model": "gpt-4",
        "max_tokens": 2000
    },
    "claude-3": {
        "provider": "anthropic",
        "model": "claude-3-opus",
        "max_tokens": 2000
    },
    "gemini": {
        "provider": "google",
        "model": "gemini-2.0-flash",
        "max_tokens": 2000
    }
}
