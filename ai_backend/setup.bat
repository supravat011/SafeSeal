@echo off
echo ========================================
echo SafeSeal AI Backend Setup
echo ========================================
echo.

echo [1/3] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo [2/3] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please configure if needed.
) else (
    echo .env file already exists.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the AI backend:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the server: python app.py
echo.
echo The AI backend will run on http://localhost:5000
echo ========================================

pause
