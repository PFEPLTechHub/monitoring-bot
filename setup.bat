@echo off
echo Setting up Monitoring Report Bot...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Run setup script
echo Running setup...
python setup.py

REM Keep window open
echo.
echo Setup completed
pause
