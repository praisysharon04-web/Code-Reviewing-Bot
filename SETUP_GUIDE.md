# 🚀 Setup & Deployment Guide - Smart Code Reviewer Bot

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Running the Application](#running-the-application)
3. [API Testing](#api-testing)
4. [Deployment Options](#deployment-options)
5. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/code-reviewer-bot.git
cd code-reviewer-bot
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

Create `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# LLM Provider (mock = free, no API key needed)
LLM_PROVIDER=mock

# Optional: For paid LLM providers
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# HUGGINGFACE_API_KEY=hf_...

# Server Settings
PORT=8000
HOST=0.0.0.0
```

### Step 5: Verify Installation

```bash
# Test imports
python -c "import fastapi; import streamlit; import aiohttp; print('✅ All dependencies installed!')"
```

---

## Running the Application

### Option 1: Web UI (Streamlit) - **Recommended for testing**

```bash
streamlit run ui/app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

Open `http://localhost:8501` in your browser!

### Option 2: REST API Server

```bash
# Method 1: Direct Python
python api/main.py

# Method 2: Uvicorn with auto-reload
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
```

Open `http://localhost:8000/docs` for API documentation!

### Option 3: Run Both Simultaneously

**Terminal 1:**
```bash
python api/main.py
```

**Terminal 2:**
```bash
streamlit run ui/app.py
```

Then access:
- **Web UI**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## API Testing

### Test with cURL

```bash
# Simple review
curl -X POST "http://localhost:8000/review" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"world\")",
    "detailed": true
  }'
```

### Test with Python

```python
import requests
import json

url = "http://localhost:8000/review"

payload = {
    "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    """,
    "detailed": True
}

response = requests.post(url, json=payload)
result = response.json()

print(json.dumps(result, indent=2))
```

### Test with httpie

```bash
http POST http://localhost:8000/review \
  code="def hello(): print('world')" \
  detailed:=true
```

### Check API Health

```bash
curl http://localhost:8000/health
```

---

## Deployment Options

### 🟢 Option 1: Streamlit Cloud (Easiest, FREE)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repo
   - Enter: `ui/app.py` as main file
   - Deploy!

3. **Your app is live!**
   - Share URL: `https://your-app-name.streamlit.app`

**Pros:** Free, simple, auto-deploys on push  
**Cons:** Limited customization, Streamlit-specific

---

### 🟡 Option 2: Railway (Recommended)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "Create New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Set Environment Variables**
   - Go to Project → Variables
   - Add: `LLM_PROVIDER=mock` (or your API keys)
   - Add: `PORT=8000`

4. **Deploy**
   - Railway auto-deploys on push!
   - Your API URL: `https://your-project.up.railway.app`

5. **Test**
   ```bash
   curl https://your-project.up.railway.app/health
   ```

**Pros:** Free tier, auto-deploys, simple  
**Cons:** Limited free resources

---

### 🔵 Option 3: Docker + Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows/Linux: Download from heroku.com/download
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create code-reviewer-bot
   ```

4. **Push Docker Image**
   ```bash
   heroku container:push web
   heroku container:release web
   ```

5. **Check Logs**
   ```bash
   heroku logs --tail
   ```

6. **Your API is live!**
   ```bash
   curl https://code-reviewer-bot.herokuapp.com/health
   ```

---

### 🟣 Option 4: DigitalOcean App Platform

1. **Create Account** at [digitalocean.com](https://digitalocean.com)

2. **Create New App**
   - Click "Apps" → "Create App"
   - Connect GitHub repo
   - Configure build command: `pip install -r requirements.txt`
   - HTTP port: 8000
   - Deploy!

3. **Access Your App**
   - DigitalOcean provides a public URL

**Cost:** $5-12/month

---

### 🔴 Option 5: AWS (Production-grade)

1. **Push Docker image to ECR**
2. **Create ECS cluster**
3. **Deploy with load balancing**
4. **Setup auto-scaling**

[Detailed AWS guide](https://docs.aws.amazon.com/ecs/latest/developerguide/docker-basics.html)

---

## Deployment Comparison

| Platform | Cost | Ease | Best For | Setup Time |
|----------|------|------|----------|-----------|
| Streamlit Cloud | FREE | ⭐⭐⭐⭐⭐ | Demos, UIs | 2 min |
| Railway | FREE tier | ⭐⭐⭐⭐ | APIs, Full-stack | 5 min |
| Heroku | $7+/month | ⭐⭐⭐⭐ | Production APIs | 10 min |
| DigitalOcean | $5+/month | ⭐⭐⭐ | Production | 15 min |
| AWS | Variable | ⭐⭐ | Scale, Enterprise | 30 min |

**My Recommendation:** Start with **Streamlit Cloud** for the UI, then deploy API to **Railway** for production.

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: `Port 8000 is already in use`

**Solution:**
```bash
# Kill process using port 8000
lsof -i :8000  # Find PID
kill -9 <PID>

# Or use different port
python api/main.py --port 8001
```

### Issue: `OPENAI_API_KEY not found`

**Solution:**
```bash
# Add to .env file
echo "OPENAI_API_KEY=sk-..." >> .env

# Or export directly
export OPENAI_API_KEY=sk-...
```

### Issue: Streamlit app won't load

**Solution:**
```bash
# Clear cache
rm -rf ~/.streamlit/
streamlit run ui/app.py --logger.level=debug
```

### Issue: LLM API returning errors

**Solution:**
1. Check API key is valid
2. Check rate limits
3. Use `LLM_PROVIDER=mock` for testing
4. Check error in logs: `heroku logs --tail`

---

## Performance Tips

### For Local Development
- Use `--reload` flag for auto-restart on changes
- Use `mock` provider for fast testing
- Run in terminal for better error visibility

### For Production
- Use production ASGI server (Gunicorn + Uvicorn)
- Enable caching layer (Redis)
- Add rate limiting
- Monitor with Sentry/DataDog
- Use `LLM_PROVIDER=openai` or `claude` for quality

### Run with Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app
```

---

## Next Steps

1. ✅ Setup complete!
2. ✅ Run locally and test
3. ✅ Deploy to Streamlit Cloud or Railway
4. ✅ Get API key from OpenAI/Claude/Hugging Face
5. ✅ Update environment variables
6. ✅ Share with recruiters!

**GitHub URL**: `https://github.com/yourusername/code-reviewer-bot`  
**Live Demo**: `https://your-app-name.streamlit.app`  
**API Endpoint**: `https://your-project.up.railway.app`

---

## Questions?

- Check [FAQ](FAQ.md)
- Open an Issue on GitHub
- Check [Discussions](https://github.com/yourusername/code-reviewer-bot/discussions)

Happy deploying! 🚀
