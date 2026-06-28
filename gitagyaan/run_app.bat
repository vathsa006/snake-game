@echo off
REM Bhagavad Gita QA System - Windows Launcher
REM This script makes it easy to run the application on Windows

echo ====================================
echo  Bhagavad Gita QA System
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version
echo.

REM Check if requirements are installed
echo [2/3] Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo.
    echo Required libraries not found. Installing...
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Try running: pip install -r requirements.txt
        pause
        exit /b 1
    )
) else (
    echo All dependencies are installed!
)
echo.

REM Launch the Streamlit app
echo [3/3] Launching application...
echo.
echo Your browser will open automatically.
echo To stop the app, close this window or press Ctrl+C
echo.
echo ====================================
echo.

streamlit run app.py

pause
