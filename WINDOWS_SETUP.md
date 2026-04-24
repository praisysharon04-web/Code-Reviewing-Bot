# 🪟 Windows Complete Setup Guide

## ⚡ FASTEST WAY (2 steps only!)

### **Step 1: Download ALL Files**

Download these 14 files and save them to ONE folder on your Desktop:

1. `setup.bat` ← **MAIN SETUP SCRIPT** ⭐
2. `setup.py`
3. `requirements.txt`
4. `README.md`
5. `.gitignore`
6. `Dockerfile`
7. `src_reviewer.py`
8. `src_llm_provider.py`
9. `api_main.py`
10. `ui_app.py`
11. `examples_usage.py`
12. `QUICKSTART.md`
13. `SETUP_GUIDE.md`
14. `CODE_REVIEWER_GUIDE.md`

**Create folder structure:**
```
Desktop/code-reviewer-bot/
├── setup.bat
├── setup.py
├── requirements.txt
├── README.md
├── .gitignore
├── Dockerfile
├── src_reviewer.py
├── src_llm_provider.py
├── api_main.py
├── ui_app.py
└── examples_usage.py
```

---

### **Step 2: Run setup.bat**

1. **Right-click** on `setup.bat`
2. Click **"Run as administrator"**
3. **Wait for it to finish** (2-5 minutes)
4. Press any key when done

**What it does automatically:**
- ✅ Creates all folders (src, api, ui, examples, tests)
- ✅ Creates virtual environment
- ✅ Installs all Python packages
- ✅ Verifies everything works

---

## 🎉 After setup.bat Completes

The script will tell you the next step. Here's what to do:

### **Step 3: Copy Files to Right Folders**

The `setup.bat` created the folders, but you need to organize the Python files.

**Open File Explorer** and move these files:

- `src_reviewer.py` → Move to `src\` folder → Rename to `reviewer.py`
- `src_llm_provider.py` → Move to `src\` folder → Rename to `llm_provider.py`
- `api_main.py` → Move to `api\` folder → Rename to `main.py`
- `ui_app.py` → Move to `ui\` folder → Rename to `app.py`
- `examples_usage.py` → Move to `examples\` folder → Rename to `usage_examples.py`

**Quick way (drag and drop):**
1. Open File Explorer
2. Open `code-reviewer-bot` folder
3. Open `src` folder (in another window)
4. Drag `src_reviewer.py` into `src` folder
5. Right-click it → Rename to `reviewer.py`
6. Repeat for other files

---

### **Step 4: Activate & Run**

Open **Command Prompt** and go to your folder:

```bash
cd Desktop\code-reviewer-bot
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal.

Run the app:

```bash
streamlit run ui/app.py
```

---

### **Step 5: Open in Browser**

When you see:
```
Local URL: http://localhost:8501
```

**Copy and paste that URL into your browser!** 🎉

---

## 📋 File Organization Checklist

After following the steps above, your folder should look like:

```
Desktop/code-reviewer-bot/
├── venv/                          ← Created by setup.bat
├── src/
│   ├── __init__.py               ← Created by setup.bat
│   ├── reviewer.py               ← YOU organize this
│   └── llm_provider.py           ← YOU organize this
├── api/
│   ├── __init__.py
│   └── main.py                   ← YOU organize this
├── ui/
│   ├── __init__.py
│   └── app.py                    ← YOU organize this
├── examples/
│   ├── __init__.py
│   └── usage_examples.py         ← YOU organize this
├── tests/
│   └── __init__.py
├── .env                          ← Created by setup.bat
├── setup.bat                     ← Run this first!
├── setup.py
├── requirements.txt
├── README.md
├── .gitignore
└── Dockerfile
```

---

## ✅ Quick Command Reference

After setup is done, these are the main commands:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run web UI
streamlit run ui/app.py

# Run REST API server
python api/main.py

# Deactivate virtual environment (when done)
deactivate
```

---

## ❌ Troubleshooting

### "Python is not installed"
Install from: https://www.python.org/downloads/
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Restart Command Prompt and try again

### "setup.bat doesn't run"
1. Right-click on `setup.bat`
2. Click "Run as administrator"
3. Click "Yes" if asked for permission

### "Files are in wrong places"
Use File Explorer to manually organize them:
- `src_reviewer.py` → `src\reviewer.py`
- `src_llm_provider.py` → `src\llm_provider.py`
- `api_main.py` → `api\main.py`
- `ui_app.py` → `ui\app.py`
- `examples_usage.py` → `examples\usage_examples.py`

### "venv\Scripts\activate doesn't work"
Try:
```bash
venv\Scripts\Activate.ps1
```

### "streamlit command not found"
Make sure you:
1. See `(venv)` at start of terminal
2. Ran `pip install -r requirements.txt` successfully

Try:
```bash
python -m streamlit run ui/app.py
```

---

## 🎮 Test It Works

After running `streamlit run ui/app.py`:

1. Open: http://localhost:8501
2. Paste this code:
```python
def hello():
    print("world")
```
3. Click **"🔍 Review Code"**
4. See AI feedback appear! ✨

---

## 📊 Project Structure Created

```
code-reviewer-bot/
├── venv/                    (Python environment)
├── src/                     (Core logic)
│   ├── reviewer.py         (Code analyzer)
│   └── llm_provider.py     (LLM API handlers)
├── api/                     (REST API)
│   └── main.py             (FastAPI server)
├── ui/                      (Web interface)
│   └── app.py              (Streamlit app)
├── examples/                (Example usage)
│   └── usage_examples.py   (7 usage examples)
├── tests/                   (Unit tests)
└── Config files            (README, requirements, etc.)
```

---

## 🚀 Next Steps (After Testing)

1. **Try different code**: Paste various code snippets
2. **Get API key** (optional): Add OpenAI/Claude key to .env
3. **Deploy to internet**: 
   - Streamlit Cloud (web UI)
   - Railway (REST API)
4. **Share on GitHub**: Show recruiters your code
5. **Practice interview pitch**: Explain what you built

---

## ⚠️ Important Notes

- Virtual environment (`venv`) is large (~500MB) - don't upload to GitHub
- `.gitignore` will automatically exclude it ✓
- `setup.bat` only needs to run ONCE
- Always activate `venv` before running anything
- Keep `setup.bat` and `setup.py` in the root folder

---

## 🎯 Expected Time

- Setup: 5 minutes (setup.bat does most work)
- Organizing files: 5 minutes (drag and drop)
- Running app: 1 minute
- **Total: ~10 minutes!** ⚡

---

## 📞 Quick Help

**Something not working?** Run this to check your setup:

```bash
python setup.py
```

This will:
- Check all files are in right places
- Create missing files
- Verify everything is correct

---

**Now go download the files and run `setup.bat`!** 🚀

You'll have everything running in 10 minutes! 💪
