# 🤖 Smart Code Reviewer Bot

An AI-powered code review system that analyzes code snippets and provides intelligent feedback on quality, bugs, optimization, and more.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🎯 Features

- **Multi-Language Support**: Review Python, JavaScript, Java, C++, Go, Rust, and more
- **Comprehensive Analysis**:
  - Code quality assessment with scoring
  - Bug and security vulnerability detection
  - Code explanation and purpose analysis
  - Performance optimization suggestions
  - Complexity analysis (time, space, cyclomatic)
- **Multiple LLM Backends**: OpenAI (GPT-4), Anthropic Claude, Hugging Face, or mock for testing
- **REST API**: Production-ready FastAPI server
- **Web UI**: Beautiful Streamlit interface for easy use
- **Batch Processing**: Review multiple code snippets at once
- **Review History**: Track and retrieve past reviews

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda
- (Optional) API key for OpenAI, Claude, or Hugging Face

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/code-reviewer-bot.git
cd code-reviewer-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 1. **Web UI (Recommended for getting started)**

```bash
streamlit run ui/app.py
```

Then open `http://localhost:8501` in your browser.

#### 2. **REST API**

```bash
python api/main.py
```

Server runs on `http://localhost:8000`

**API Documentation**: Visit `http://localhost:8000/docs` for interactive Swagger UI

**Example request:**
```bash
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
    "detailed": true
  }'
```

#### 3. **Python Module (Programmatic use)**

```python
import asyncio
from src.reviewer import CodeReviewer
from src.llm_provider import get_llm_provider

async def main():
    # Initialize with mock provider (no API key needed)
    llm = get_llm_provider("mock")
    reviewer = CodeReviewer(llm)
    
    code = """
    def hello():
        print('world')
    """
    
    result = await reviewer.review_code(code)
    print(result)

asyncio.run(main())
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# LLM Provider choice: "openai", "claude", "huggingface", or "mock"
LLM_PROVIDER=mock

# API Keys (only needed for respective providers)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_API_KEY=hf_...

# Server settings
PORT=8000
HOST=0.0.0.0
```

### Switching LLM Providers

**Option 1: Environment Variable**
```bash
export LLM_PROVIDER=openai
python api/main.py
```

**Option 2: Direct initialization**
```python
from src.llm_provider import get_llm_provider

# OpenAI
llm = get_llm_provider("openai", model="gpt-4")

# Claude
llm = get_llm_provider("claude", model="claude-3-sonnet-20240229")

# Hugging Face (free, open-source)
llm = get_llm_provider("huggingface", model="mistralai/Mistral-7B-Instruct-v0.1")

# Mock (for testing)
llm = get_llm_provider("mock")
```

## 📊 API Endpoints

### Submit a Review
```
POST /review
Content-Type: application/json

{
  "code": "python code here",
  "detailed": true
}

Response:
{
  "review_id": "a1b2c3d4",
  "status": "success",
  "detected_language": "python",
  "code_length": 150,
  "review": {
    "code_quality": {...},
    "bugs_security": {...},
    "explanation": {...},
    "optimization": {...},
    "complexity": {...}
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### Get Review by ID
```
GET /review/{review_id}
```

### List Recent Reviews
```
GET /reviews?limit=10
```

### Batch Review
```
POST /batch-review
Content-Type: application/json

{
  "codes": ["code1", "code2", "code3"]
}
```

### Health Check
```
GET /health
```

## 📁 Project Structure

```
code-reviewer-bot/
├── src/
│   ├── reviewer.py          # Core review logic
│   └── llm_provider.py      # LLM API handlers
├── api/
│   └── main.py              # FastAPI server
├── ui/
│   └── app.py               # Streamlit web UI
├── tests/
│   ├── test_reviewer.py
│   └── test_api.py
├── examples/
│   └── sample_reviews.json
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── Dockerfile              # Container setup
```

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/

# Async test example
pytest tests/test_reviewer.py::test_review_code -v
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t code-reviewer-bot .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  code-reviewer-bot
```

## 🚢 Deployment Options

### **Streamlit Cloud** (Easiest, Free)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy directly from GitHub

### **Heroku** (Easy, Free tier available)
```bash
heroku create code-reviewer-bot
git push heroku main
```

### **Railway** (Recommended, Simple)
1. Connect GitHub repository
2. Set environment variables
3. Deploy!

### **AWS / GCP / Azure** (Production)
- Use Docker container with Kubernetes
- Set up load balancing and auto-scaling

## 💡 Interview Talking Points

### "Tell me about this project"
*"I built an AI-powered code review system that analyzes code snippets and provides intelligent feedback on quality, bugs, optimization, and complexity. It supports multiple programming languages and LLM providers (OpenAI, Claude, Hugging Face). The backend is a FastAPI server with a Streamlit UI, and it's designed to be scalable and production-ready."*

### "What was the most challenging part?"
*"Managing LLM context length for large code files and balancing accuracy vs. cost. I implemented prompt engineering techniques to get consistent, structured JSON responses from different LLM providers. Also, handling edge cases like different code formatting and language detection."*

### "How would you scale this?"
*"I'd implement:*
- *Async job queue (Celery) for long-running reviews*
- *Redis caching for duplicate code snippets*
- *Database (PostgreSQL) to store review history*
- *Multi-model ensemble for different analysis types*
- *API rate limiting and user authentication*
- *Monitoring with Prometheus and error tracking with Sentry"*

### "What did you learn?"
*"Working with multiple LLM APIs and their different response formats, prompt engineering best practices, async Python, REST API design, and deployment considerations. Also learned about the trade-offs between model quality, cost, and latency."*

## 📈 Performance

- **Average review time**: 1-3 seconds (depends on LLM)
- **Max code size**: 10,000 characters
- **Batch processing**: Up to 100 snippets per request
- **API response time**: <100ms (excluding LLM call)

## 🔒 Security Considerations

- Validate and sanitize all user inputs
- Use environment variables for API keys (never hardcode)
- Rate limit API endpoints
- Add authentication for production
- Strip sensitive information from code before sending to LLM
- Use HTTPS in production

## 🐛 Known Limitations

- LLM responses can occasionally be inconsistent
- Very long code files (>10KB) may be truncated
- Some edge case programming languages not detected
- Free tier LLMs may have quality trade-offs

## 🛣️ Roadmap

- [ ] Support for more programming languages
- [ ] GitHub integration (review PRs automatically)
- [ ] Custom review rules and templates
- [ ] Code clone detection
- [ ] Performance benchmarking
- [ ] Team collaboration features
- [ ] VS Code extension
- [ ] IDE plugins (PyCharm, IntelliJ)

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [Claude API](https://docs.anthropic.com/)
- [Hugging Face](https://huggingface.co/)

## 📄 License

MIT License - See `LICENSE` file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 💬 Questions?

Feel free to open an issue or start a discussion. Happy coding! 🚀

---

**Built with ❤️ for Big Four interviews**
