# services/browsebench/metrics.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TestResult:
    test_name: str
    success: bool
    steps: int
    response_time: float
    token_usage: int
    cost: float
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BenchmarkResults:
    total_tests: int
    completed_tests: int
    completion_rate: float
    average_steps: float
    average_response_time: float
    total_token_usage: int
    total_cost: float
    results: List[TestResult] = field(default_factory=list)

class MetricsCollector:
    def __init__(self):
        self.results: List[TestResult] = []

    def add_result(self, result: TestResult):
        self.results.append(result)

    def aggregate_results(self) -> BenchmarkResults:
        total_tests = len(self.results)
        if not total_tests:
            return BenchmarkResults(0, 0, 0.0, 0.0, 0.0, 0, 0.0)

        completed_tests = sum(1 for r in self.results if r.success)
        completion_rate = completed_tests / total_tests
        average_steps = sum(r.steps for r in self.results) / total_tests
        average_response_time = sum(r.response_time for r in self.results) / total_tests
        total_token_usage = sum(r.token_usage for r in self.results)
        total_cost = sum(r.cost for r in self.results)

        return BenchmarkResults(
            total_tests=total_tests,
            completed_tests=completed_tests,
            completion_rate=completion_rate,
            average_steps=average_steps,
            average_response_time=average_response_time,
            total_token_usage=total_token_usage,
            total_cost=total_cost,
            results=self.results
        )
