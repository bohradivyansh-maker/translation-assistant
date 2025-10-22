# 🚀 Translation Assistant - Complete User Guide

**A Context-Aware Translation Tool for Windows**

This guide explains how to install and use the Translation Assistant on Windows, whether you have Python installed or not.

---

## 📋 Table of Contents

1. [For Non-Python Users (Easiest Method)](#for-non-python-users-easiest-method)
2. [For Python Users (From Source)](#for-python-users-from-source)
3. [How to Use the Application](#how-to-use-the-application)
4. [Features Overview](#features-overview)
5. [Troubleshooting](#troubleshooting)
6. [Frequently Asked Questions](#frequently-asked-questions)

---

## 🎯 For Non-Python Users (Easiest Method)

**No Python installation required! Just download and run.**

### Option 1: Download Pre-Built Executable (Recommended)

1. **Download the Application**
   - Go to the [Releases](https://github.com/bohradivyansh-maker/translation-assistant/releases) page
   - Download `TranslationAssistant-Standalone.zip` (latest version)
   - File size: ~340 MB (includes all dependencies)

2. **Extract the ZIP File**
   - Right-click on the downloaded ZIP file
   - Select "Extract All..."
   - Choose a destination folder (e.g., `C:\Programs\TranslationAssistant`)
   - Click "Extract"

3. **Run the Application**
   - Navigate to the extracted folder
   - Double-click `TranslationAssistant.exe`
   - First run may take 10-15 seconds to start

4. **Windows Defender Warning** (if appears)
   - Click "More info"
   - Click "Run anyway"
   - This warning appears because the app is not signed (normal for personal projects)

### Option 2: Build Executable Yourself

If you prefer to build it yourself:

1. **Install Python 3.13+** from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   
2. **Download Source Code**
   ```cmd
   # Download as ZIP from GitHub or clone:
   git clone https://github.com/bohradivyansh-maker/translation-assistant.git
   cd translation-assistant
   ```

3. **Run Build Script**
   ```cmd
   build_executable.bat
   ```
   - Build time: 10-20 minutes
   - Output: `portable_executable\TranslationAssistant-Standalone.zip`

---

## 🐍 For Python Users (From Source)

### Prerequisites

- **Python 3.7 or higher** (Tested on Python 3.13.7)
- **Windows 10/11** (64-bit)
- **Internet connection** (for initial setup)

### Step 1: Download the Project

**Method A: Using Git**
```bash
git clone https://github.com/bohradivyansh-maker/translation-assistant.git
cd translation-assistant
```

**Method B: Download ZIP**
1. Go to [GitHub Repository](https://github.com/bohradivyansh-maker/translation-assistant)
2. Click "Code" → "Download ZIP"
3. Extract to a folder (e.g., `C:\Projects\translation-assistant`)
4. Open Command Prompt in that folder

### Step 2: Automated Setup (Recommended)

```cmd
setup.bat
```

This script will:
- Create a virtual environment
- Install all dependencies (16 packages)
- Download spaCy language model (en_core_web_sm)
- Download NLTK data packages
- Verify installation
- Takes 5-10 minutes

### Step 3: Manual Setup (Alternative)

If `setup.bat` doesn't work:

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

### Step 4: Run the Application

**Using the Start Script:**
```cmd
start_app.bat
```

**Or manually:**
```cmd
venv\Scripts\activate
python main.py
```

---

## 💡 How to Use the Application

### First Launch

1. **Start the Application**
   - Run `TranslationAssistant.exe` (standalone version)
   - OR run `start_app.bat` (Python version)
   
2. **Status Window Appears**
   - A small window appears in the bottom-right corner
   - Shows: "Translation Assistant Running"
   - This window can be minimized

3. **Application is Now Active**
   - Runs in the background
   - Ready to translate text from any application

### Basic Translation Workflow

```
1. Select text anywhere (browser, Word, Notepad, etc.)
2. Press Ctrl+Shift+T
3. Choose target language from popup
4. Translation appears in a popup window
5. Listen to audio (optional)
```

### Detailed Steps

#### Step 1: Select Text to Translate

- **Works in any Windows application:**
  - Web browsers (Chrome, Edge, Firefox)
  - Microsoft Word, Excel, PowerPoint
  - Notepad, Notepad++, VS Code
  - PDFs, emails, chat applications
  
- **How to select:**
  - Click and drag to highlight text
  - Or use keyboard: Shift + Arrow keys
  - Or double-click to select a word
  - Or Ctrl+A to select all

#### Step 2: Trigger Translation

- **Press the hotkey:** `Ctrl + Shift + T`
- **What happens:**
  - Selected text is automatically copied
  - Language selector popup appears
  - You have 10 seconds to choose (or press ESC to cancel)

#### Step 3: Choose Target Language

- **Available Languages (16):**
  - 🇬🇧 English
  - 🇪🇸 Spanish (Español)
  - 🇫🇷 French (Français)
  - 🇩🇪 German (Deutsch)
  - 🇮🇹 Italian (Italiano)
  - 🇵🇹 Portuguese (Português)
  - 🇷🇺 Russian (Русский)
  - 🇯🇵 Japanese (日本語)
  - 🇰🇷 Korean (한국어)
  - 🇨🇳 Chinese Simplified (简体中文)
  - 🇹🇼 Chinese Traditional (繁體中文)
  - 🇸🇦 Arabic (العربية)
  - 🇮🇳 Hindi (हिन्दी)
  - 🇹🇷 Turkish (Türkçe)
  - 🇳🇱 Dutch (Nederlands)
  - 🇸🇪 Swedish (Svenska)

- **Selection Methods:**
  - Click the language button
  - Or press the number key (1-16)
  - Or press ESC to cancel

#### Step 4: View Translation

- **Translation popup shows:**
  - Original text
  - Detected source language
  - Translated text
  - Key terms extracted from original
  - Named entities (people, places, organizations)

- **Popup Features:**
  - 🔊 **Play Audio** button - Listen to translation (Text-to-Speech)
  - 📋 **Copy** button - Copy translation to clipboard
  - ❌ **Close** button - Close the popup
  - Auto-closes after 30 seconds (or click anywhere)

### Advanced Features

#### Translation Memory

- **Automatic saving:**
  - Every translation is saved to a local database
  - Speeds up repeated translations
  - No internet needed for previously translated text

- **How it works:**
  - Original text → Checked against memory
  - If match found → Instant translation
  - If not found → Translate & save to memory

#### Context Analysis

- **Automatic analysis includes:**
  - **Named Entity Recognition (NER):**
    - People: "Albert Einstein", "Marie Curie"
    - Places: "Paris", "United States"
    - Organizations: "Google", "United Nations"
    
  - **Part-of-Speech (POS) Tagging:**
    - Identifies nouns, verbs, adjectives
    - Preserves grammatical structure
    
  - **Key Term Extraction (TF-IDF):**
    - Identifies most important words
    - Shows context-specific vocabulary
    - Up to 5 key terms displayed

#### Custom Dictionary

- **Location:** `data/custom_dictionary.json`
- **Purpose:** Define custom translations for specific terms
- **Format:**
  ```json
  {
    "technical_term": "translated_term",
    "brand_name": "brand_name"
  }
  ```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Shift + T` | Trigger translation |
| `Ctrl + Shift + Q` | Exit application |
| `ESC` | Cancel language selection |
| `1-16` | Quick language selection (in selector) |

---

## 🎨 Features Overview

### 1. **Context-Aware Translation**
- Understands context using NLP techniques
- Preserves meaning, not just word-by-word translation
- Handles idioms and phrases intelligently

### 2. **Multi-Language Support**
- 16 languages available
- Automatic source language detection
- High-quality translations using Google Translate API

### 3. **Named Entity Recognition**
- Identifies and preserves proper nouns
- Recognizes:
  - Person names
  - Location names
  - Organization names
  - Dates and numbers

### 4. **Translation Memory**
- SQLite database stores all translations
- Instant retrieval for repeated text
- Works offline for saved translations
- Automatic cleanup of old entries

### 5. **Key Term Extraction**
- TF-IDF algorithm finds important words
- Shows technical vocabulary
- Helps understand context
- Up to 5 terms displayed

### 6. **Audio Playback**
- Text-to-Speech (TTS) using gTTS
- Natural-sounding voice
- Supports all 16 languages
- Helps with pronunciation

### 7. **System-Wide Hotkeys**
- Works in any Windows application
- Global keyboard shortcuts
- Background operation
- Minimal resource usage

### 8. **User-Friendly Interface**
- Clean, modern design
- Large, readable text
- Emoji flags for languages
- Timeout warnings
- Dark mode compatible

---

## 🔧 Troubleshooting

### Issue: Application Won't Start

**Symptoms:** Double-clicking .exe does nothing

**Solutions:**
1. **Check Windows Defender:**
   - Open Windows Security
   - Go to "Virus & threat protection"
   - Check "Protection history"
   - If blocked, allow the application

2. **Run as Administrator:**
   - Right-click `TranslationAssistant.exe`
   - Select "Run as administrator"

3. **Check for missing dependencies:**
   ```cmd
   # For Python version
   python -m pip install -r requirements.txt --force-reinstall
   ```

### Issue: Hotkey Not Working (Ctrl+Shift+T)

**Symptoms:** Nothing happens when pressing Ctrl+Shift+T

**Solutions:**
1. **Check if another application is using the hotkey:**
   - Close other apps that might use global hotkeys
   - Try restarting the Translation Assistant

2. **Make sure text is selected:**
   - Highlight text before pressing hotkey
   - Test in Notepad first

3. **Verify application is running:**
   - Check for status window in bottom-right
   - Check Task Manager for "TranslationAssistant.exe"

4. **Reinstall pynput:**
   ```cmd
   pip uninstall pynput
   pip install pynput==1.7.6
   ```

### Issue: Translation Returns Garbage Text

**Symptoms:** Translation shows mixed languages or strange characters

**Solutions:**
1. **Update to latest version** - This issue was fixed in recent updates

2. **Check internet connection** - Translation requires internet

3. **Try a different language** - Some language pairs work better

4. **Simplify the text** - Break long paragraphs into sentences

### Issue: Audio Not Playing

**Symptoms:** "Play Audio" button doesn't work

**Solutions:**
1. **Check system volume** - Ensure volume is not muted

2. **Check speakers/headphones** - Test with other audio

3. **Reinstall audio dependencies:**
   ```cmd
   pip uninstall gtts playsound3
   pip install gtts==2.5.0 playsound3==3.2.8
   ```

4. **Check audio file location:**
   - Look for `translation_audio.mp3` in project folder
   - Make sure folder is not read-only

### Issue: "Module Not Found" Error

**Symptoms:** Error message: "ModuleNotFoundError: No module named 'X'"

**Solutions:**
1. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

2. **Reinstall dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Check Python version:**
   ```cmd
   python --version
   # Should be 3.7 or higher
   ```

### Issue: Application Freezes

**Symptoms:** Application stops responding

**Solutions:**
1. **Force quit using exit hotkey:**
   - Press `Ctrl + Shift + Q`

2. **Kill via Task Manager:**
   - Press `Ctrl + Shift + Esc`
   - Find "TranslationAssistant.exe" or "python.exe"
   - Click "End Task"

3. **Restart the application**

### Issue: High Memory Usage

**Symptoms:** Application uses too much RAM

**Solutions:**
1. **Clear translation memory:**
   - Delete `translation_memory.db`
   - Restart application

2. **Use standalone .exe version:**
   - More efficient than Python version

3. **Close other applications:**
   - Free up system resources

---

## ❓ Frequently Asked Questions

### General Questions

**Q: Does this work offline?**
A: Partially. Translation memory works offline for previously translated text. New translations require internet connection.

**Q: Is my data sent to any servers?**
A: Only to Google Translate API for translation. Nothing else is sent. All data stored locally.

**Q: Can I use this commercially?**
A: This project is for educational/personal use. Check Google Translate API terms for commercial use.

**Q: What languages are supported?**
A: 16 languages: English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese (Simplified/Traditional), Arabic, Hindi, Turkish, Dutch, Swedish.

**Q: Can I add more languages?**
A: Yes! Edit `src/language_selector.py` and add language codes to the `LANGUAGES` dictionary.

**Q: How do I uninstall?**
A: Simply delete the application folder. No registry entries or system files are created.

### Technical Questions

**Q: Which NLP techniques are used?**
A: 
- Named Entity Recognition (spaCy)
- Part-of-Speech Tagging (NLTK)
- TF-IDF Term Extraction (scikit-learn)
- Translation Memory (SQLite)

**Q: Why is the .exe file so large (340 MB)?**
A: It includes Python interpreter, all libraries, and the spaCy language model (en_core_web_sm ~15MB).

**Q: Can I change the hotkey?**
A: Yes! Edit `src/hotkey_handler.py` and modify the `_is_hotkey_pressed()` method.

**Q: Does it support right-to-left languages?**
A: Yes! Arabic and Hebrew are supported with proper RTL rendering.

**Q: Can I run multiple instances?**
A: No. Only one instance can run at a time due to global hotkey registration.

### Performance Questions

**Q: How fast is the translation?**
A: 
- From memory: Instant (<100ms)
- New translation: 1-3 seconds (depends on internet speed)

**Q: How much RAM does it use?**
A: 
- Python version: 150-250 MB
- Standalone .exe: 200-300 MB

**Q: Does it slow down my computer?**
A: No. Minimal CPU usage when idle. Only active during translation.

### Privacy & Security

**Q: Is this application safe?**
A: Yes. Source code is open and available on GitHub for review.

**Q: Where is data stored?**
A: Locally in `translation_memory.db` (SQLite database) in the application folder.

**Q: Can I delete translation history?**
A: Yes. Delete `translation_memory.db` file. It will be recreated on next run.

**Q: Does it collect analytics?**
A: No. Zero telemetry. No data collection.

---

## 📞 Support & Contributing

### Getting Help

- **GitHub Issues:** [Report bugs or request features](https://github.com/bohradivyansh-maker/translation-assistant/issues)
- **Email:** Contact the developer for support
- **Documentation:** Check README.md for developer documentation

### Contributing

Contributions are welcome! See `CONTRIBUTING.md` for guidelines.

**Ways to contribute:**
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation
- Add new language support

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## 🙏 Acknowledgments

- **spaCy** - Natural Language Processing
- **NLTK** - Tokenization and POS tagging
- **deep-translator** - Translation engine
- **Google Translate** - Translation API
- **PyInstaller** - Executable creation

---

## 📚 Additional Resources

- [Project Repository](https://github.com/bohradivyansh-maker/translation-assistant)
- [Developer Documentation](README.md)
- [API Documentation](https://github.com/bohradivyansh-maker/translation-assistant/wiki)
- [Video Tutorial](#) (Coming soon)

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Author:** Divyansh Bohra  
**Project:** NLP Course Assignment

---

## 🚀 Quick Start Summary

### For Non-Programmers:
1. Download `TranslationAssistant-Standalone.zip` from Releases
2. Extract ZIP file
3. Run `TranslationAssistant.exe`
4. Select text anywhere and press `Ctrl+Shift+T`

### For Python Users:
1. `git clone https://github.com/bohradivyansh-maker/translation-assistant.git`
2. `cd translation-assistant`
3. `setup.bat`
4. `start_app.bat`
5. Select text and press `Ctrl+Shift+T`

**That's it! Happy translating! 🌍**
