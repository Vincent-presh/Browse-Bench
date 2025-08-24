# BrowseBench: AI Web Agent Benchmark

## 🎯 Overview

BrowseBench is an open-source benchmark for evaluating AI model capabilities in web browsing and agentic tasks. It leverages OpenRouter infrastructure to test multiple AI models on standardized web automation tasks, providing a comprehensive evaluation framework for web agents.

## 🚀 Core Requirements

### 1. **Multi-Model Testing Infrastructure**

- OpenRouter integration for seamless model switching
- Support for: GPT-4, Claude, Gemini, OSS models
- Standardized API interface for all models
- Configurable model parameters and constraints

### 2. **Four Core Test Categories**

- **Navigation & Discovery**: Find specific information across multiple pages
- **Form Interaction**: Complete forms with validation and error handling
- **Multi-Step Workflows**: Execute complex, multi-page tasks
- **Robustness Testing**: Handle dynamic content, popups, and errors

### 3. **Standardized Evaluation Metrics**

- Task completion rate
- Steps efficiency (optimal path vs actual)
- Error recovery capability
- Response time and token usage
- Cost analysis per model

## 🏗️ Architecture

### **Benchmark Runner**

```python
# services/browsebench/runner.py
class BrowseBenchRunner:
    def __init__(self, model_config: ModelConfig):
        self.model = self._setup_model(model_config)
        self.playwright = self._setup_browser()
        self.metrics = MetricsCollector()

    async def run_benchmark(self, test_suite: TestSuite) -> BenchmarkResults:
        results = []
        for test in test_suite.tests:
            result = await self._execute_test(test)
            results.append(result)
        return self._aggregate_results(results)
```

### **Test Suite Definition**

```yaml
# tests/navigation_test.yaml
name: "Navigation & Discovery"
description: "Find product information across multiple pages"
url: "https://demo-ecommerce.com"
goal: "Extract product name, price, and availability from search results"
constraints:
  - "Use only navigation tools"
  - "Don't click on ads"
  - "Handle pagination if needed"
oracle:
  - "Product name found"
  - "Price extracted correctly"
  - "Availability status determined"
```

### **Model Configuration**

```python
# config/models.py
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
```

## 📋 Implementation Plan

### **Phase 1: Core Infrastructure (Week 1-2)**

1. Create `services/browsebench/` directory
2. Implement `BrowseBenchRunner` class
3. Set up OpenRouter integration
4. Create basic test framework
5. Set up Playwright browser automation

### **Phase 2: Test Suite (Week 3-4)**

1. Implement four core test scenarios
2. Create synthetic test sites (demo-ecommerce, demo-blog, etc.)
3. Build oracle validation system
4. Add metrics collection
5. Implement error handling and recovery

### **Phase 3: Evaluation & Reporting (Week 5-6)**

1. Implement results aggregation
2. Create leaderboard system
3. Add detailed analytics dashboard
4. Write documentation and examples
5. Set up CI/CD pipeline

## 📁 File Structure

```
services/browsebench/
├── __init__.py
├── runner.py              # Main benchmark runner
├── test_suite.py          # Test definition and execution
├── metrics.py             # Performance metrics collection
├── models.py              # AI model configuration
├── oracles.py             # Test validation logic
├── config/                # Configuration files
│   ├── models.py
│   └── settings.py
└── tests/                 # Test definitions
    ├── navigation_test.yaml
    ├── form_test.yaml
    ├── workflow_test.yaml
    └── robustness_test.yaml
```

## 🔧 Key Features

### **Deterministic Testing**

- Fixed seed generation for reproducible results
- Synthetic test sites with controlled variables
- Standardized browser state management
- Consistent evaluation environment

### **Extensible Framework**

- Easy addition of new test scenarios
- Custom model configurations
- Plugin system for new evaluation metrics
- Support for custom test sites

### **Open Source Ready**

- MIT license
- Comprehensive documentation
- Docker setup for easy deployment
- GitHub Actions for CI/CD
- Contributing guidelines

## 📊 Success Metrics

- **Accuracy**: 95%+ test completion rate on baseline models
- **Performance**: <30 seconds average task completion
- **Reliability**: <5% variance across multiple runs
- **Adoption**: 100+ GitHub stars within 3 months
- **Community**: Active contributors and model submissions

## 🌐 Test Scenarios

### **1. Navigation & Discovery**

- **Goal**: Find specific information across multiple pages
- **Example**: "Find the pricing page and extract all plan details"
- **Success Criteria**: Correct information extracted, efficient path taken

### **2. Form Interaction**

- **Goal**: Complete forms with validation and error handling
- **Example**: "Fill out contact form and handle validation errors"
- **Success Criteria**: Form submitted successfully, errors handled gracefully

### **3. Multi-Step Workflows**

- **Goal**: Execute complex, multi-page tasks
- **Example**: "Search for a product, add to cart, and proceed to checkout"
- **Success Criteria**: All steps completed in correct order

### **4. Robustness Testing**

- **Goal**: Handle dynamic content, popups, and errors
- **Example**: "Navigate through site with popup ads and dynamic loading"
- **Success Criteria**: Task completed despite interruptions

## 🚀 Getting Started

### **Prerequisites**

- Python 3.8+
- Playwright
- OpenRouter API key
- Docker (optional)

### **Quick Start**

```bash
# Clone repository
git clone https://github.com/your-org/browsebench.git
cd browsebench

# Install dependencies
pip install -r requirements.txt

# Set up environment
export OPENROUTER_API_KEY="your-key-here"

# Run benchmark
python -m browsebench.runner --model gpt-4
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code style and standards
- Test development
- Documentation updates
- Bug reports and feature requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](https://browsebench.readthedocs.io)
- [Issues](https://github.com/your-org/browsebench/issues)
- [Discussions](https://github.com/your-org/browsebench/discussions)
- [Releases](https://github.com/your-org/browsebench/releases)

## 📞 Support

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and community support
- **Email**: browsebench@your-org.com

---

**BrowseBench** - The definitive benchmark for AI web agents. 🚀
