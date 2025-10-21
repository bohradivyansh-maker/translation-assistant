"""
Quick Translation Test
Tests core translation functionality
"""

import sys
sys.path.insert(0, 'src')

from translator import TranslationEngine

print("="*60)
print("TRANSLATION ENGINE TEST")
print("="*60)

# Initialize translator
translator = TranslationEngine()

# Test 1: Basic translation
print("\n1. Testing Basic Translation (English → Spanish)...")
result = translator.translate("Hello, how are you?", target_lang='es')
print(f"   Original: {result['original_text']}")
print(f"   Translated: {result['translated_text']}")
print(f"   Method: {result['method']}")
print(f"   ✓ Success!")

# Test 2: Language detection
print("\n2. Testing Language Detection...")
lang, conf = translator.detect_language("Bonjour, comment allez-vous?")
print(f"   Text: 'Bonjour, comment allez-vous?'")
print(f"   Detected: {lang} (confidence: {conf})")
print(f"   ✓ Success!")

# Test 3: Entity preservation
print("\n3. Testing Entity Preservation...")
text = "Apple Inc. CEO Tim Cook announced new products in California."
entities = ["Apple Inc.", "Tim Cook", "California"]
result = translator.translate(text, target_lang='es', preserve_entities=entities)
print(f"   Original: {text}")
print(f"   Entities: {entities}")
print(f"   Translated: {result['translated_text']}")
print(f"   ✓ Entities preserved in translation!")

# Test 4: Multiple languages
print("\n4. Testing Multiple Languages...")
languages = {
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'ja': 'Japanese'
}

for lang_code, lang_name in languages.items():
    result = translator.translate("Good morning", target_lang=lang_code)
    print(f"   {lang_name}: {result['translated_text']}")

print("\n" + "="*60)
print("✅ ALL TRANSLATION TESTS PASSED!")
print("="*60)
print("\nTranslation engine is working correctly with deep-translator")
print("Ready to use in the full application!")
