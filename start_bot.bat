@echo off
echo Starting Monitoring Report Bot...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found
    echo Please run setup.py first or copy env.example to .env
    pause
    exit /b 1
)

REM Start the bot
echo Starting bot...
python start_bot.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Bot stopped with an error
    pause
)
