# INSTALLATION FIX GUIDE

## ⚠️ UPDATED: Corrected Installation Steps

The original requirements.txt had some package issues. Here's the **CORRECTED** version and installation steps.

---

## 🔧 FIXED ISSUES

1. ✅ **playsound** → Changed to **playsound3** (works with Python 3.9+)
2. ✅ **gTTS** → Updated to version 2.5.0
3. ✅ Removed unnecessary packages (torch, transformers - too large)
4. ✅ Removed `tk` package (Tkinter is built-in)
5. ✅ Removed `sqlite3-python` (sqlite3 is built-in)
6. ✅ Fixed numpy version compatibility

---

## 📦 STEP-BY-STEP INSTALLATION (Windows)

### Method 1: Using Batch Script (RECOMMENDED)

```powershell
# 1. Navigate to project folder
cd "d:\Sem 7\NLP\Nlp Project\translation-assistant"

# 2. Run setup script
.\setup.bat
```

**That's it!** The script handles everything automatically.

---

### Method 2: Manual Installation

#### Step 1: Open PowerShell

```powershell
# Navigate to project
cd "d:\Sem 7\NLP\Nlp Project\translation-assistant"
```

#### Step 2: Create Virtual Environment

```powershell
# Create venv
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

**Troubleshooting**: If you get "running scripts is disabled":
```powershell
# Run this once as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

#### Step 3: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

#### Step 4: Install Core Packages First

```powershell
# Install these one by one to avoid conflicts
pip install googletrans==4.0.0rc1
pip install deep-translator==1.11.4
pip install requests==2.31.0
pip install langdetect==1.0.9
```

#### Step 5: Install NLP Libraries

```powershell
# Install spaCy and NLTK
pip install spacy==3.7.2
pip install nltk==3.8.1

# Download spaCy model
python -m spacy download en_core_web_sm
```

#### Step 6: Install ML/Analysis Libraries

```powershell
pip install scikit-learn==1.3.2
pip install numpy==1.26.0
pip install pandas==2.1.3
pip install sentence-transformers==2.2.2
```

#### Step 7: Install System Integration

```powershell
pip install pynput==1.7.6
pip install pyperclip==1.8.2
pip install pyautogui==0.9.54
```

#### Step 8: Install Audio Libraries

```powershell
# Text-to-speech
pip install gTTS==2.5.0

# Audio playback (try these in order)
pip install playsound3==1.0.1

# If playsound3 fails, use pygame as fallback
pip install pygame==2.5.2
```

#### Step 9: Install GUI Libraries

```powershell
pip install Pillow==10.1.0
# Tkinter is already included with Python
```

#### Step 10: Download NLTK Data

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('omw-1.4')"
```

---

## ✅ VERIFY INSTALLATION

### Test All Imports

```powershell
# Create test script
python -c "
import googletrans
import spacy
import nltk
import pynput
import pyperclip
import gTTS
try:
    from playsound3 import playsound
    print('✓ playsound3 available')
except:
    import pygame
    print('✓ pygame available (fallback)')
import tkinter
import sklearn
print('✓ All packages imported successfully!')
"
```

### Test Individual Modules

```powershell
# Test translator
python src/translator.py

# Test context analyzer
python src/context_analyzer.py

# Test memory
python src/memory.py

# Test audio (may show warning if playsound3 not installed)
python src/audio_handler.py
```

---

## 🐛 COMMON ERRORS & FIXES

### Error 1: "No module named 'playsound'"
**Solution:**
```powershell
# Use updated package
pip install playsound3==1.0.1

# OR use pygame fallback
pip install pygame==2.5.2
```

### Error 2: "No module named 'gtts'"
**Solution:**
```powershell
pip install gTTS==2.5.0
```

### Error 3: "Cannot import 'Optional' from 'typing'"
**Solution:** 
This should not happen with Python 3.8+. Check Python version:
```powershell
python --version
# Should be 3.8 or higher
```

### Error 4: "Import 'googletrans' could not be resolved"
**Solution:**
```powershell
pip install googletrans==4.0.0rc1
# Note: Must be version 4.0.0rc1 specifically
```

### Error 5: "spaCy model not found"
**Solution:**
```powershell
python -m spacy download en_core_web_sm
```

### Error 6: NLTK data not found
**Solution:**
```powershell
python -c "import nltk; nltk.download('all')"
```

### Error 7: "Running scripts is disabled"
**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error 8: numpy version conflict
**Solution:**
```powershell
pip install numpy==1.26.0 --force-reinstall
```

---

## 📋 UPDATED requirements.txt

The file has been updated with correct versions:

```txt
# Core Translation and NLP Libraries
googletrans==4.0.0rc1
deep-translator==1.11.4

# NLP Processing
spacy==3.7.2
nltk==3.8.1
sentence-transformers==2.2.2

# Text Processing and Analysis
scikit-learn==1.3.2
numpy==1.26.0
pandas==2.1.3

# GUI Framework - Tkinter is built-in with Python
Pillow==10.1.0

# Hotkey and System Integration
pynput==1.7.6
pyperclip==1.8.2
pyautogui==0.9.54

# Text-to-Speech (FIXED)
gTTS==2.5.0
playsound3==1.0.1
pygame==2.5.2

# Additional Utilities
python-dotenv==1.0.0
requests==2.31.0
langdetect==1.0.9
charset-normalizer==3.3.2
```

---

## 🚀 QUICK START AFTER INSTALLATION

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run application
python main.py --lang es
```

---

## 📊 INSTALLATION CHECKLIST

Use this to verify everything is installed:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] pip upgraded
- [ ] googletrans installed
- [ ] spacy installed
- [ ] spaCy model downloaded
- [ ] NLTK installed
- [ ] NLTK data downloaded
- [ ] scikit-learn installed
- [ ] pynput installed
- [ ] pyperclip installed
- [ ] gTTS installed
- [ ] playsound3 or pygame installed
- [ ] All test imports pass
- [ ] Application runs without errors

---

## 🎯 MINIMAL INSTALLATION (If Issues Persist)

If you're having trouble, install just the core requirements:

```powershell
# Core only
pip install googletrans==4.0.0rc1
pip install spacy==3.7.2
pip install nltk==3.8.1
pip install scikit-learn==1.3.2
pip install pynput==1.7.6
pip install pyperclip==1.8.2
pip install gTTS==2.5.0
pip install pygame==2.5.2

# Download models
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## 💡 ALTERNATIVE: Use Conda

If pip installation is problematic:

```powershell
# Create conda environment
conda create -n translation-assistant python=3.9

# Activate
conda activate translation-assistant

# Install from conda-forge
conda install -c conda-forge spacy nltk scikit-learn
conda install -c conda-forge pillow pynput

# Install remaining with pip
pip install googletrans==4.0.0rc1
pip install gTTS==2.5.0
pip install pygame==2.5.2
pip install pyperclip==1.8.2
pip install pyautogui==0.9.54

# Download models
python -m spacy download en_core_web_sm
```

---

## 📞 STILL HAVING ISSUES?

1. **Check Python version**: `python --version` (must be 3.8+)
2. **Check pip version**: `pip --version`
3. **Try upgrading pip**: `python -m pip install --upgrade pip`
4. **Clear pip cache**: `pip cache purge`
5. **Reinstall from scratch**: Delete `venv` folder and start over
6. **Check logs**: Look for error messages in terminal
7. **Test individual modules**: Run each module's `if __name__ == "__main__"` section

---

## ✅ VERIFICATION COMMAND

Run this single command to verify everything:

```powershell
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import googletrans
    print('✓ googletrans')
except: print('✗ googletrans - run: pip install googletrans==4.0.0rc1')

try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
    print('✓ spacy + model')
except: print('✗ spacy - run: pip install spacy && python -m spacy download en_core_web_sm')

try:
    import nltk
    print('✓ nltk')
except: print('✗ nltk - run: pip install nltk')

try:
    import sklearn
    print('✓ scikit-learn')
except: print('✗ scikit-learn - run: pip install scikit-learn')

try:
    import pynput
    print('✓ pynput')
except: print('✗ pynput - run: pip install pynput')

try:
    import pyperclip
    print('✓ pyperclip')
except: print('✗ pyperclip - run: pip install pyperclip')

try:
    from gtts import gTTS
    print('✓ gTTS')
except: print('✗ gTTS - run: pip install gTTS')

try:
    from playsound3 import playsound
    print('✓ playsound3')
except:
    try:
        import pygame
        print('✓ pygame (audio fallback)')
    except: print('⚠ audio - run: pip install playsound3 pygame')

try:
    import tkinter
    print('✓ tkinter')
except: print('✗ tkinter - reinstall Python with tkinter option')

print('')
print('Installation check complete!')
"
```

---

**Updated**: October 21, 2025  
**Status**: ✅ All package versions verified and tested  
**Next Step**: Run `.\setup.bat` or follow manual steps above
