from dataclasses import dataclass

@dataclass
class ModelConfig:
    provider: str
    model: str
    max_tokens: int

MODEL_CONFIGS = {
    "gpt-4": {
        "provider": "openai",
        "model": "openai/gpt-4",
        "max_tokens": 4096
    },
    "claude-3-opus": {
        "provider": "anthropic",
        "model": "anthropic/claude-3-opus",
        "max_tokens": 4096
    },
    "gemini-flash": {
        "provider": "google",
        "model": "google/gemini-flash-1.5",
        "max_tokens": 8192
    },
    "gemini-pro": {
        "provider": "google",
        "model": "google/gemini-pro",
        "max_tokens": 8192
    }
}