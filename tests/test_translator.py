"""
Unit tests for Translation Engine
"""

import unittest
from src.translator import TranslationEngine


class TestTranslationEngine(unittest.TestCase):
    """Test cases for translation engine"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize translator once for all tests"""
        cls.translator = TranslationEngine()
    
    def test_language_detection(self):
        """Test language detection"""
        # English
        lang, conf = self.translator.detect_language("Hello, how are you?")
        self.assertEqual(lang, 'en')
        self.assertGreater(conf, 0.5)
        
        # Spanish
        lang, conf = self.translator.detect_language("Hola, ¿cómo estás?")
        self.assertEqual(lang, 'es')
        self.assertGreater(conf, 0.5)
    
    def test_simple_translation(self):
        """Test simple translation"""
        result = self.translator.translate(
            "Hello, world!",
            target_lang='es'
        )
        
        self.assertIn('translated_text', result)
        self.assertEqual(result['target_language'], 'es')
        self.assertGreater(len(result['translated_text']), 0)
    
    def test_entity_preservation(self):
        """Test entity preservation during translation"""
        result = self.translator.translate(
            "John Smith works at Microsoft",
            target_lang='es',
            preserve_entities=['John Smith', 'Microsoft']
        )
        
        # Check entities are preserved
        self.assertIn('John Smith', result['translated_text'])
        self.assertIn('Microsoft', result['translated_text'])
    
    def test_same_language_translation(self):
        """Test translation when source equals target"""
        result = self.translator.translate(
            "Hello",
            source_lang='en',
            target_lang='en'
        )
        
        self.assertEqual(result['original_text'], result['translated_text'])
        self.assertEqual(result['method'], 'no_translation_needed')
    
    def test_supported_languages(self):
        """Test supported languages list"""
        languages = self.translator.get_supported_languages()
        
        self.assertIn('en', languages)
        self.assertIn('es', languages)
        self.assertIn('fr', languages)
        self.assertGreater(len(languages), 5)
    
    def test_language_support_check(self):
        """Test language support checking"""
        self.assertTrue(self.translator.is_language_supported('en'))
        self.assertTrue(self.translator.is_language_supported('es'))
        self.assertFalse(self.translator.is_language_supported('xyz'))


if __name__ == '__main__':
    unittest.main()
