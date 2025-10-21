@echo off
REM Quick fix for Python 3.13 compatibility issues
REM This script removes the old venv and reinstalls everything

echo ============================================================
echo   Python 3.13 Compatibility Fix
echo ============================================================
echo.
echo This will:
echo   1. Delete your existing virtual environment
echo   2. Create a fresh virtual environment
echo   3. Install all packages (without pygame)
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/5] Removing old virtual environment...
if exist venv (
    rmdir /s /q venv
    echo Old venv removed!
) else (
    echo No existing venv found, skipping...
)
echo.

echo [2/5] Creating fresh virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created!
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/5] Upgrading build tools...
python -m pip install --upgrade pip setuptools wheel
echo.

echo [5/5] Installing packages from requirements.txt...
echo This may take 5-10 minutes...
echo.

pip install googletrans==4.0.0rc1
pip install deep-translator==1.11.4
pip install spacy==3.7.2
pip install nltk==3.8.1
pip install sentence-transformers==2.2.2
pip install scikit-learn==1.3.2
pip install numpy==1.26.0
pip install pandas==2.1.3
pip install Pillow==10.1.0
pip install pynput==1.7.6
pip install pyperclip==1.8.2
pip install pyautogui==0.9.54
pip install gTTS==2.5.0
pip install playsound3==1.0.1
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install langdetect==1.0.9
pip install charset-normalizer==3.3.2

echo.
echo ========================================
echo   Downloading NLP Models
echo ========================================
echo.

echo [6/7] Downloading spaCy language model...
python -m spacy download en_core_web_sm
if %ERRORLEVEL% neq 0 (
    echo WARNING: Failed to download spaCy model
    echo You can try again later with: python -m spacy download en_core_web_sm
)
echo.

echo [7/7] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
if %ERRORLEVEL% neq 0 (
    echo WARNING: Failed to download NLTK data
    echo You can try again later by running: python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
)
echo.

echo ============================================================
echo   Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Run: python test_installation.py
echo   2. If all tests pass, run: python main.py
echo.
echo Note: pygame was removed due to Python 3.13 compatibility
echo       Audio will use playsound3 only (this is fine!)
echo.
pause
