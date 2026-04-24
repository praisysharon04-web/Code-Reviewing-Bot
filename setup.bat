@echo off
REM ============ Smart Code Reviewer Bot - Automatic Setup for Windows ============
REM This script sets up everything automatically!

echo.
echo ========================================
echo   CODE REVIEWER BOT - AUTO SETUP
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Creating folder structure...
if not exist "src" mkdir src
if not exist "api" mkdir api
if not exist "ui" mkdir ui
if not exist "examples" mkdir examples
if not exist "tests" mkdir tests
echo       ✓ Folders created

echo.
echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo       ✓ Virtual environment created
) else (
    echo       ✓ Virtual environment already exists
)

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo       ✓ Virtual environment activated

echo.
echo [4/5] Installing Python packages...
echo       (This may take 2-5 minutes, please wait...)
pip install -q -r requirements.txt
if errorlevel 1 (
    echo       ✗ ERROR: Failed to install packages
    pause
    exit /b 1
)
echo       ✓ All packages installed

echo.
echo [5/5] Verifying installation...
python -c "import fastapi, streamlit, aiohttp; print('       ✓ All dependencies verified')" 2>nul
if errorlevel 1 (
    echo       ✗ WARNING: Some packages may not be installed
)

echo.
echo ========================================
echo   SETUP COMPLETE! ✓
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Make sure these files are in the right folders:
echo    - src\reviewer.py (from src_reviewer.py)
echo    - src\llm_provider.py (from src_llm_provider.py)
echo    - api\main.py (from api_main.py)
echo    - ui\app.py (from ui_app.py)
echo    - examples\usage_examples.py (from examples_usage.py)
echo.
echo 2. Run the app with:
echo    streamlit run ui/app.py
echo.
echo 3. Open in browser:
echo    http://localhost:8501
echo.
pause
