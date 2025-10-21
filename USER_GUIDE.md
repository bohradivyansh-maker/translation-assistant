# 🌐 Translation Assistant - User Guide

## ✨ Easy Exit - Problem Solved!

Your translation assistant now has **3 easy ways to exit**:

---

## 🚪 How to Close the Application

### **Method 1: Exit Hotkey (Fastest!)**
Press **`Ctrl+Shift+Q`** anytime to close the app instantly.

### **Method 2: Status Window Button**
1. Find the status window in the bottom-right corner
2. Click the **"Exit App"** button (red button)

### **Method 3: Status Window Menu**
1. Right-click the status window
2. Select "Exit" or close normally

---

## 🎮 Using the Application

### Starting the App
- **Double-click** `start_app.bat` (or `TranslationAssistant.exe`)
- A small status window appears in the bottom-right corner
- The app is now running and listening for hotkeys

### Translating Text
1. **Select any text** in any application (browser, Word, PDF, etc.)
2. **Press `Ctrl+Shift+T`**
3. **Choose your target language** from the popup menu
4. **View translation** instantly!

### Status Window
- Shows green indicator when app is running
- Can be **minimized** (app keeps working in background)
- Can be **moved** anywhere on screen
- Displays keyboard shortcuts

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **`Ctrl+Shift+T`** | Translate selected text |
| **`Ctrl+Shift+Q`** | Exit application |
| **`ESC`** | Use default language (skip language selector) |

---

## 🌍 Supported Languages

The app supports translation to 16 languages:

- 🇬🇧 English (**NEW!**)
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇮🇳 Hindi
- 🇯🇵 Japanese
- 🇨🇳 Chinese
- 🇸🇦 Arabic
- 🇵🇹 Portuguese
- 🇷🇺 Russian
- 🇮🇹 Italian
- 🇰🇷 Korean
- 🇹🇷 Turkish
- 🇳🇱 Dutch
- 🇵🇱 Polish
- 🇻🇳 Vietnamese

---

## 💡 Pro Tips

1. **Minimize the status window** - The app keeps working in the background
2. **Use `Ctrl+Shift+Q` for quick exit** - No need to find the window
3. **ESC for English** - Skip language selector to translate to English instantly
4. **Works everywhere** - Try it in browser, Word, PDFs, emails, anywhere!
5. **Translation memory** - Repeated phrases translate instantly (cached)

---

## ❓ Common Questions

### **Q: How do I know the app is running?**
A: Look for the status window in the bottom-right corner with a green indicator 🟢

### **Q: Can I minimize the status window?**
A: Yes! Click "Minimize" button. The app keeps running in background.

### **Q: The app won't close from Task Manager - is this fixed?**
A: Yes! Now you can use `Ctrl+Shift+Q` or the Exit button to close properly.

### **Q: Does the app use resources when idle?**
A: Very minimal! <1% CPU, ~150MB RAM. It just listens for hotkeys.

### **Q: What if I forget the hotkeys?**
A: Check the status window - they're displayed there!

### **Q: Can I change the hotkeys?**
A: Currently set to `Ctrl+Shift+T` (translate) and `Ctrl+Shift+Q` (exit). Can be customized in code.

---

## 🐛 Troubleshooting

### App Won't Start
- Make sure Python 3.11+ is installed (for .bat version)
- For `.exe` version, run as Administrator if blocked
- Check `translation_assistant.log` for errors

### Hotkey Not Working
- Ensure app is running (check status window)
- Another app might be using the same hotkey
- Try closing other translation or hotkey apps

### App Won't Exit
- Use **`Ctrl+Shift+Q`** (new exit hotkey)
- Or click **Exit App** button in status window
- If still stuck, close from Task Manager (should not happen now!)

### Status Window Missing
- Check if it's minimized in taskbar
- Look in bottom-right corner of screen
- Restart the app if needed

### Translation Errors
- Check internet connection (needed for translation API)
- View detailed errors in `translation_assistant.log`

---

## 📊 Features Summary

✅ **Context-aware translation** - Preserves names, dates, and entities  
✅ **15 language support** - Major world languages  
✅ **Translation memory** - Caches frequent translations  
✅ **Works system-wide** - Any application  
✅ **Easy exit** - Multiple ways to close  
✅ **Minimal resources** - Runs efficiently in background  
✅ **Visual feedback** - Status window and popups  
✅ **Keyboard-driven** - Fast workflow with hotkeys  

---

## 🎓 For Academic Use

**NLP Concepts Demonstrated:**
- Named Entity Recognition (NER) - Preserves person/location names
- Context Analysis - Detects domain (technical, formal, casual)
- Translation Memory - Caches and reuses translations
- Language Detection - Auto-detects source language
- Term Extraction - Identifies key terms and phrases

**Technologies Used:**
- **NLP:** spaCy, NLTK
- **Translation:** deep-translator (Google Translate API)
- **GUI:** Tkinter
- **Hotkeys:** pynput
- **Audio:** gTTS, playsound3
- **ML:** scikit-learn (TF-IDF)

---

## 📝 Credits

**NLP Mini Project - October 2025**

Translation Assistant with Context Analysis, NER, and Multi-language Support

---

**Enjoy hassle-free translation! 🌍✨**

*Remember: Press `Ctrl+Shift+Q` anytime to exit!*
