# 📖 Translation Assistant - Quick Reference Card

**Print this page or keep it handy while using the application!**

---

## ⚡ Installation (Choose One)

### Option A: For Non-Python Users (Easiest)
```
1. Download TranslationAssistant-Standalone.zip
2. Extract ZIP
3. Run TranslationAssistant.exe
```

### Option B: For Python Users
```cmd
git clone https://github.com/bohradivyansh-maker/translation-assistant.git
cd translation-assistant
setup.bat
start_app.bat
```

---

## 🎯 Basic Usage

### Step 1: Start Application
- Double-click `TranslationAssistant.exe`
- Or run `start_app.bat` (Python version)
- Status window appears in bottom-right corner

### Step 2: Translate Text
```
1. Select any text (anywhere in Windows)
2. Press Ctrl+Shift+T
3. Choose language from popup
4. View translation + listen to audio
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Shift + T` | **Start Translation** |
| `Ctrl + Shift + Q` | **Exit Application** |
| `ESC` | Cancel language selector |
| `1-16` | Quick select language (in popup) |

---

## 🌍 Supported Languages (16)

| # | Language | Code | # | Language | Code |
|---|----------|------|---|----------|------|
| 1 | 🇬🇧 English | en | 9 | 🇰🇷 Korean | ko |
| 2 | 🇪🇸 Spanish | es | 10 | 🇨🇳 Chinese (S) | zh-CN |
| 3 | 🇫🇷 French | fr | 11 | 🇹🇼 Chinese (T) | zh-TW |
| 4 | 🇩🇪 German | de | 12 | 🇸🇦 Arabic | ar |
| 5 | 🇮🇹 Italian | it | 13 | 🇮🇳 Hindi | hi |
| 6 | 🇵🇹 Portuguese | pt | 14 | 🇹🇷 Turkish | tr |
| 7 | 🇷🇺 Russian | ru | 15 | 🇳🇱 Dutch | nl |
| 8 | 🇯🇵 Japanese | ja | 16 | 🇸🇪 Swedish | sv |

---

## 🎨 Translation Popup Features

```
┌─────────────────────────────────────┐
│  Original Text: [Your text here]    │
│  Detected Language: French          │
├─────────────────────────────────────┤
│  Translation:                        │
│  [Translated text appears here]     │
├─────────────────────────────────────┤
│  Key Terms: word1, word2, word3     │
│  Entities: Name, Place, Org         │
├─────────────────────────────────────┤
│  [🔊 Play Audio] [📋 Copy] [❌ Close]│
└─────────────────────────────────────┘
```

**Features:**
- 🔊 **Play Audio** - Listen to translation
- 📋 **Copy** - Copy to clipboard
- Auto-closes in 30 seconds

---

## 🚨 Common Issues & Quick Fixes

### Issue: Hotkey not working
**Fix:** Make sure text is selected first, then press `Ctrl+Shift+T`

### Issue: No translation appears
**Fix:** Check internet connection (required for new translations)

### Issue: Application won't start
**Fix:** 
- Run as Administrator (right-click → Run as administrator)
- Check Windows Defender didn't block it

### Issue: Can't close application
**Fix:** Press `Ctrl+Shift+Q` or kill via Task Manager

### Issue: Audio not playing
**Fix:** Check system volume, ensure speakers/headphones connected

---

## 📁 File Locations

```
translation-assistant/
├── TranslationAssistant.exe    ← Main application (standalone)
├── start_app.bat                ← Start script (Python version)
├── translation_memory.db        ← Saved translations
├── data/
│   └── custom_dictionary.json   ← Custom term definitions
└── HOW_TO_USE.md               ← Full user guide
```

---

## 🔧 Advanced Tips

### Add Custom Translations
Edit `data/custom_dictionary.json`:
```json
{
  "technical_term": "your_translation",
  "brand_name": "brand_name"
}
```

### Change Hotkey
Edit `src/hotkey_handler.py` and modify:
```python
# Change Ctrl+Shift+T to your preferred combination
if ctrl and shift and (hasattr(k, 'char') and k.char == 't'):
```

### Clear Translation History
Delete `translation_memory.db` and restart

### Works In These Apps
✅ Chrome, Edge, Firefox  
✅ Microsoft Word, Excel  
✅ Notepad, VS Code  
✅ PDF readers  
✅ Email clients  
✅ **Any Windows application!**

---

## 💡 Pro Tips

1. **Use Translation Memory:** Translate common phrases once, get instant results later
2. **Key Terms Help:** Check extracted terms to understand context
3. **Audio Learning:** Use "Play Audio" to learn pronunciation
4. **Quick Selection:** Press number keys (1-16) in language selector for faster workflow
5. **Minimize Status Window:** It runs in the background, no need to keep visible

---

## 📊 Performance Stats

| Metric | Value |
|--------|-------|
| Translation Speed | 1-3 seconds (new) |
| Memory Usage | ~250 MB |
| Startup Time | 5-10 seconds |
| Supported Languages | 16 |
| Max Text Length | Unlimited |
| Offline Capability | Yes (for saved translations) |

---

## 🆘 Need More Help?

📖 **Full Guide:** `HOW_TO_USE.md`  
📚 **Developer Docs:** `README.md`  
🐛 **Report Bug:** [GitHub Issues](https://github.com/bohradivyansh-maker/translation-assistant/issues)  
💬 **Contact:** Email the developer

---

## 📌 Quick Troubleshooting Checklist

Before asking for help, check:
- [ ] Application is running (status window visible)
- [ ] Text is selected before pressing hotkey
- [ ] Internet connection is active
- [ ] Windows Defender hasn't blocked the app
- [ ] No other app is using Ctrl+Shift+T
- [ ] Virtual environment is activated (Python version)

---

## 🎓 Educational Use

**Perfect for:**
- Students learning foreign languages
- Researchers reading papers in other languages
- Translators needing quick references
- Language teachers demonstrating translations
- Anyone working with multilingual content

---

**Version:** 1.0.0  
**GitHub:** [bohradivyansh-maker/translation-assistant](https://github.com/bohradivyansh-maker/translation-assistant)

---

## 🎯 Remember: The Magic Formula

```
1. SELECT TEXT
2. Ctrl + Shift + T
3. CHOOSE LANGUAGE
4. DONE! 🎉
```

**Print this page for quick reference!** 🖨️
