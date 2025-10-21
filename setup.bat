@echo off
REM Context-Aware Translation Assistant - Windows Setup Script
REM This script automates the complete setup process

echo ============================================================
echo   Context-Aware Translation Assistant - Setup
echo ============================================================
echo.

REM Check Python installation
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.
echo NOTE: Python 3.12+ removed 'distutils' module
echo       Some packages may need pre-built wheels
echo.

REM Create virtual environment
echo [2/7] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip and build tools
echo [4/7] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
echo.

REM Install dependencies
echo [5/7] Installing Python packages...
echo This may take a few minutes...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may have failed to install
    echo Trying critical packages individually...
    echo.
    pip install googletrans==4.0.0rc1
    pip install spacy==3.7.2
    pip install nltk==3.8.1
    pip install scikit-learn==1.3.2
    pip install pynput==1.7.6
    pip install pyperclip==1.8.2
    pip install gTTS==2.5.0
    pip install pygame==2.5.2
)
echo.

REM Download spaCy model
echo [6/7] Downloading spaCy language model...
python -m spacy download en_core_web_sm
echo.

REM Download NLTK data
echo [7/7] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('omw-1.4', quiet=True)"
echo.

echo ============================================================
echo   Verifying Installation...
echo ============================================================
echo.
python -c "import googletrans; print('✓ googletrans')" 2>nul || echo ✗ googletrans
python -c "import spacy; print('✓ spacy')" 2>nul || echo ✗ spacy
python -c "import nltk; print('✓ nltk')" 2>nul || echo ✗ nltk
python -c "import sklearn; print('✓ scikit-learn')" 2>nul || echo ✗ scikit-learn
python -c "import pynput; print('✓ pynput')" 2>nul || echo ✗ pynput
python -c "import pyperclip; print('✓ pyperclip')" 2>nul || echo ✗ pyperclip
python -c "from gtts import gTTS; print('✓ gTTS')" 2>nul || echo ✗ gTTS
python -c "try: from playsound3 import playsound; print('✓ playsound3')\nexcept: import pygame; print('✓ pygame (audio)')" 2>nul || echo ⚠ audio (optional)
python -c "import tkinter; print('✓ tkinter')" 2>nul || echo ✗ tkinter
echo.

echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo To start the application:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run: python main.py --lang es
echo.
echo Quick start: run.bat
echo.
echo For help: python main.py --help
echo For examples: python examples.py
echo.
echo If you had installation errors, check: INSTALLATION_FIX.md
echo ============================================================
pause
