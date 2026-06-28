#!/bin/bash

# Bhagavad Gita QA System - Unix Launcher
# This script makes it easy to run the application on Linux/Mac

echo "===================================="
echo " Bhagavad Gita QA System"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "[1/3] Checking Python installation..."
python3 --version
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip3"
    exit 1
fi

# Check if requirements are installed
echo "[2/3] Checking dependencies..."
if ! pip3 show streamlit &> /dev/null; then
    echo ""
    echo "Required libraries not found. Installing..."
    echo "This may take a few minutes..."
    echo ""
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies"
        echo "Try running: pip3 install -r requirements.txt"
        exit 1
    fi
else
    echo "All dependencies are installed!"
fi
echo ""

# Launch the Streamlit app
echo "[3/3] Launching application..."
echo ""
echo "Your browser will open automatically."
echo "To stop the app, press Ctrl+C"
echo ""
echo "===================================="
echo ""

streamlit run app.py
