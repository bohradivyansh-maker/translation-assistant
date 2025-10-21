"""
Quick Installation Test Script
Verifies all required packages are installed correctly
"""

import sys

print("="*60)
print("INSTALLATION VERIFICATION TEST")
print("="*60)
print(f"\nPython Version: {sys.version}")
print(f"Python Path: {sys.executable}")
print("\nTesting package imports...\n")

# Track results
passed = []
failed = []
warnings = []

# Test 1: Core Translation
print("1. Testing Core Translation Libraries...")
try:
    import googletrans
    print("   ✓ googletrans")
    passed.append("googletrans")
except Exception as e:
    # googletrans fails on Python 3.13+ due to removed 'cgi' module
    # This is expected - we use deep-translator instead
    if "cgi" in str(e):
        print(f"   ⚠ googletrans - Not compatible with Python 3.13+ (expected)")
        print("   → Using deep-translator instead (already configured)")
        warnings.append("googletrans (Python 3.13 incompatible - deep-translator used)")
    else:
        print(f"   ✗ googletrans - {e}")
        failed.append("googletrans")

try:
    import deep_translator
    print("   ✓ deep-translator")
    passed.append("deep-translator")
except Exception as e:
    print(f"   ✗ deep-translator - {e}")
    failed.append("deep-translator")

# Test 2: NLP Libraries
print("\n2. Testing NLP Libraries...")
try:
    import spacy
    print("   ✓ spacy")
    passed.append("spacy")
    
    # Test spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
        print("   ✓ spacy model (en_core_web_sm)")
        passed.append("spacy model")
    except Exception as e:
        print(f"   ✗ spacy model - {e}")
        print("   → Run: python -m spacy download en_core_web_sm")
        failed.append("spacy model")
except Exception as e:
    print(f"   ✗ spacy - {e}")
    failed.append("spacy")

try:
    import nltk
    print("   ✓ nltk")
    passed.append("nltk")
    
    # Test NLTK data
    try:
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        word_tokenize("test")
        stopwords.words('english')
        print("   ✓ nltk data")
        passed.append("nltk data")
    except Exception as e:
        print(f"   ⚠ nltk data - {e}")
        print("   → Run: python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords')\"")
        warnings.append("nltk data")
except Exception as e:
    print(f"   ✗ nltk - {e}")
    failed.append("nltk")

# Test 3: ML Libraries
print("\n3. Testing ML/Analysis Libraries...")
try:
    import sklearn
    print("   ✓ scikit-learn")
    passed.append("scikit-learn")
except Exception as e:
    print(f"   ✗ scikit-learn - {e}")
    failed.append("scikit-learn")

try:
    import numpy
    print("   ✓ numpy")
    passed.append("numpy")
except Exception as e:
    print(f"   ✗ numpy - {e}")
    failed.append("numpy")

# Test 4: System Integration
print("\n4. Testing System Integration Libraries...")
try:
    import pynput
    print("   ✓ pynput")
    passed.append("pynput")
except Exception as e:
    print(f"   ✗ pynput - {e}")
    failed.append("pynput")

try:
    import pyperclip
    print("   ✓ pyperclip")
    passed.append("pyperclip")
except Exception as e:
    print(f"   ✗ pyperclip - {e}")
    failed.append("pyperclip")

try:
    import pyautogui
    print("   ✓ pyautogui")
    passed.append("pyautogui")
except Exception as e:
    print(f"   ✗ pyautogui - {e}")
    failed.append("pyautogui")

# Test 5: Text-to-Speech
print("\n5. Testing Text-to-Speech Libraries...")
try:
    from gtts import gTTS
    print("   ✓ gTTS")
    passed.append("gTTS")
except Exception as e:
    print(f"   ✗ gTTS - {e}")
    failed.append("gTTS")

audio_found = False
try:
    from playsound3 import playsound
    print("   ✓ playsound3")
    passed.append("playsound3")
    audio_found = True
except Exception as e:
    try:
        import pygame
        print("   ✓ pygame (audio fallback)")
        passed.append("pygame")
        audio_found = True
    except Exception as e2:
        print(f"   ✗ audio playback - No playsound3 or pygame")
        print("   → Run: pip install playsound3 pygame")
        warnings.append("audio playback")

# Test 6: GUI Libraries
print("\n6. Testing GUI Libraries...")
try:
    import tkinter
    print("   ✓ tkinter (built-in)")
    passed.append("tkinter")
except Exception as e:
    print(f"   ✗ tkinter - {e}")
    print("   → Tkinter should be included with Python. Reinstall Python with tkinter.")
    failed.append("tkinter")

try:
    from PIL import Image
    print("   ✓ Pillow")
    passed.append("Pillow")
except Exception as e:
    print(f"   ✗ Pillow - {e}")
    failed.append("Pillow")

# Test 7: Additional Utilities
print("\n7. Testing Additional Utilities...")
try:
    import requests
    print("   ✓ requests")
    passed.append("requests")
except Exception as e:
    print(f"   ✗ requests - {e}")
    failed.append("requests")

try:
    import langdetect
    print("   ✓ langdetect")
    passed.append("langdetect")
except Exception as e:
    print(f"   ✗ langdetect - {e}")
    failed.append("langdetect")

# Summary
print("\n" + "="*60)
print("INSTALLATION SUMMARY")
print("="*60)
print(f"✓ Passed: {len(passed)}")
print(f"✗ Failed: {len(failed)}")
print(f"⚠ Warnings: {len(warnings)}")

if failed:
    print("\nFailed packages:")
    for pkg in failed:
        print(f"  - {pkg}")
    print("\nInstallation commands:")
    print("  pip install -r requirements.txt")
    print("  python -m spacy download en_core_web_sm")
    print("  python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords')\"")

if warnings:
    print("\nWarnings:")
    for pkg in warnings:
        print(f"  - {pkg} (optional, app may have reduced functionality)")

if not failed:
    print("\n✅ ALL REQUIRED PACKAGES INSTALLED SUCCESSFULLY!")
    print("\nYou can now run:")
    print("  python main.py --lang es")
else:
    print(f"\n⚠ {len(failed)} package(s) need to be installed.")
    print("See INSTALLATION_FIX.md for detailed instructions.")

print("="*60)
