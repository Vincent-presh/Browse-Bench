from dataclasses import dataclass, field
import json
import os
from typing import Optional

@dataclass
class ModelConfig:
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None

def load_model_configs():
    config_path = os.path.join(os.path.dirname(__file__), 'model_configs.json')
    with open(config_path, 'r') as f:
        return json.load(f)

MODEL_CONFIGS = load_model_configs()
