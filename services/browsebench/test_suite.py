# services/browsebench/test_suite.py
import yaml
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Test:
    name: str
    description: str
    url: str
    goal: str
    constraints: List[str]
    oracle: List[str]

def load_test_from_yaml(file_path: str) -> Test:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return Test(**data)

# A TestSuite could be as simple as a list of tests
TestSuite = List[Test]
