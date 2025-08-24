# BrowseBench: The Next-Generation Benchmark for AI Web Agents

![BrowseBench Banner](https://your-image-url-here.com/banner.png) <!-- Replace with a real banner -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

**BrowseBench** is a open-source benchmark designed to rigorously evaluate the capabilities of AI agents on a wide range of web browsing and automation tasks. As AI models become more powerful, it's important to understand their ability to interact with the web in a realistic, human-like way. BrowseBench provides a framework for measuring this, helping developers and researchers build more capable and robust AI agents.

## 🚀 Why BrowseBench is Important

The web is dynamic, complex, and built for humans. For AI agents to be truly useful, they need to navigate this complexity with ease. BrowseBench challenges AI models with real-world scenarios, from simple information retrieval to complex multi-step workflows. By using BrowseBench, you can:

- **Benchmark** your AI agent against leading models.
- **Identify** strengths and weaknesses in your agent's capabilities.
- **Accelerate** your research and development in agentic AI.
- **Contribute** to a community-driven effort to advance the state of the art.

## ✨ Features

- **🤖 Multi-Model Testing:** Easily switch between different AI models (e.g., GPT-4, Claude, Gemini) through OpenRouter integration.
- **📊 Standardized Metrics:** Go beyond simple task completion rates with metrics for efficiency, error recovery, and cost analysis.
- **🧩 Four Core Test Categories:** A comprehensive suite of tests covering a wide range of web interactions.
- **🔧 Extensible Framework:** Easily add new tests, models, and evaluation metrics to suit your needs.
- **🌐 Realistic Web Environments:** Tests are run on real or synthetic websites that mimic the complexity of the modern web.

## 🧪 Test Scenarios

BrowseBench includes four core categories of tests, each designed to evaluate a different aspect of an AI agent's abilities:

### 1. Navigation & Discovery

- **Goal:** Find and extract specific information from a website.
- **Example:** "Find the pricing page of a SaaS product and extract the features of each plan."

### 2. Form Interaction

- **Goal:** Complete forms, handle validation errors, and submit data.
- **Example:** "Fill out a registration form with a given set of user data and handle any validation errors that appear."

### 3. Multi-Step Workflows

- **Goal:** Execute a sequence of actions across multiple pages to achieve a high-level objective.
- **Example:** "Search for a product on an e-commerce site, add it to the cart, and navigate to the checkout page."

### 4. Robustness Testing

- **Goal:** Handle unexpected interruptions like pop-ups, dynamic content, and slow-loading elements.
- **Example:** "Navigate a news article while dismissing a subscription pop-up that appears after a delay."

## 🏁 Getting Started

Getting started with BrowseBench is easy. Here's how you can run the benchmark on your own machine:

**1. Clone the repository:**

```bash
git clone https://github.com/your-org/browsebench.git
cd browsebench
```

**2. Set up a virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
.venv/bin/playwright install
```

**4. Set up your API keys:**

```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

**5. Run the benchmark:**

```bash
.venv/bin/python -m services.browsebench.runner --model gpt-4
```

## 🤝 Contributing

We believe that the best way to advance the field of AI agents is through open collaboration. We welcome contributions from the community, whether it's adding new tests, improving the framework, or fixing bugs.

Please see our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## 📄 License

BrowseBench is licensed under the [MIT License](LICENSE).
