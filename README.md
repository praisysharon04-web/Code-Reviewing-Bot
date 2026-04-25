# 🤖 Smart Code Reviewer Bot

A free, AI-powered code review tool built with Streamlit. Paste your code and get instant feedback on quality, security, bugs, and performance — no API key required!

---

## ✨ Features

- 🔍 **Automatic language detection** — Python, JavaScript, Java, C++, Rust, Go, TypeScript
- 🛡️ **Security analysis** — detects hardcoded secrets, eval(), mutable defaults, and more
- 🐛 **Bug detection** — catches empty except blocks, bare exceptions, deep nesting
- ⚡ **Performance insights** — estimates time and space complexity
- 📊 **Code quality score** — rated out of 10
- 📈 **Analytics dashboard** — track your review history
- 💯 **100% free** — works offline, no API key needed (Mock mode)

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/your-username/code-reviewer-bot.git
cd code-reviewer-bot
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python -m streamlit run ui_app.py
```

### 5. Open in browser
```
http://localhost:8501
```

---

## 📁 Project Structure

```
code-reviewer-bot/
│
├── ui_app.py              # Streamlit web interface
├── src_reviewer.py        # Core review logic & language detection
├── src_llm_provider.py    # LLM providers (Mock, OpenAI, Claude, HuggingFace)
├── api_main.py            # FastAPI backend (optional)
├── requirements.txt       # Python dependencies
├── setup.py               # Project setup
├── Dockerfile             # Docker configuration
│
├── src/                   # Source modules
├── api/                   # API modules
├── tests/                 # Unit tests
├── examples/              # Example usage scripts
└── README.md              # This file
```

---

## 🧠 How It Works

```
You paste code
      ↓
ui_app.py (Streamlit UI)
      ↓
src_reviewer.py (detects language, builds prompt)
      ↓
src_llm_provider.py (analyzes code)
      ↓
Review displayed on screen
```

The **Mock provider** (default, free) uses rule-based static analysis to review your code locally — no internet needed.

---

## 🔍 What Gets Checked

| Category | Examples |
|----------|---------|
| **Code Quality** | Long lines, magic numbers, duplicate code, function length |
| **Security** | Hardcoded passwords, eval(), empty catch blocks, mutable defaults |
| **Bugs** | Bare except, deep nesting, unresolved TODOs |
| **Performance** | Time/space complexity estimation, nested loops |
| **Style** | Missing docstrings, type hints, print vs logging |

---

## ⚙️ LLM Providers

| Provider | Cost | API Key Required |
|----------|------|-----------------|
| **Mock** (default) | ✅ Free | ❌ No |
| OpenAI (GPT) | 💰 Paid | ✅ Yes |
| Anthropic Claude | 💰 Paid | ✅ Yes |
| Hugging Face | 🆓 Free tier | ✅ Yes |

To use a paid provider, create a `.env` file:
```
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
HUGGINGFACE_API_KEY=your-key-here
```

---

## 🛠️ Requirements

- Python 3.10+
- Windows / Mac / Linux
- Internet not required (Mock mode)

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🐳 Docker (Optional)

```bash
docker build -t code-reviewer-bot .
docker run -p 8501:8501 code-reviewer-bot
```

---

## 📝 Example Review Output

```
Code Quality Score: 7/10
Issues:
  ❌ Hardcoded password detected — use environment variables
  ❌ Deep nesting at line 5 — consider early returns

Suggestions:
  💡 Use logging instead of print()
  💡 Add type hints for better readability

Time Complexity: O(n)
Space Complexity: O(1)
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👩‍💻 Built With

- [Streamlit](https://streamlit.io) — UI framework
- [FastAPI](https://fastapi.tiangolo.com) — API backend
- [Python AST](https://docs.python.org/3/library/ast.html) — Python code analysis
- [aiohttp](https://docs.aiohttp.org) — Async HTTP client

---

> Built with ❤️ | For demonstration purposes — always review AI feedback critically.
