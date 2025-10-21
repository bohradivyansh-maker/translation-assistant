"""
Unit tests for Translation Memory
"""

import unittest
import os
import tempfile
from src.memory import TranslationMemory


class TestTranslationMemory(unittest.TestCase):
    """Test cases for translation memory"""
    
    def setUp(self):
        """Create temporary database for each test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.memory = TranslationMemory(self.temp_db.name)
    
    def tearDown(self):
        """Clean up temporary database"""
        self.memory.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_add_translation(self):
        """Test adding translation to memory"""
        translation_id = self.memory.add_translation(
            original_text="Hello",
            translated_text="Hola",
            source_lang="en",
            target_lang="es",
            confidence=0.95
        )
        
        self.assertGreater(translation_id, 0)
    
    def test_find_translation(self):
        """Test finding existing translation"""
        # Add translation
        self.memory.add_translation(
            original_text="Hello",
            translated_text="Hola",
            source_lang="en",
            target_lang="es"
        )
        
        # Find it
        found = self.memory.find_translation("Hello", "en", "es")
        
        self.assertIsNotNone(found)
        self.assertEqual(found['translated_text'], "Hola")
    
    def test_translation_not_found(self):
        """Test finding non-existent translation"""
        found = self.memory.find_translation("NonExistent", "en", "es")
        self.assertIsNone(found)
    
    def test_usage_count_increment(self):
        """Test that usage count increases on duplicate"""
        # Add same translation twice
        self.memory.add_translation(
            original_text="Test",
            translated_text="Prueba",
            source_lang="en",
            target_lang="es"
        )
        
        self.memory.add_translation(
            original_text="Test",
            translated_text="Prueba",
            source_lang="en",
            target_lang="es"
        )
        
        # Check usage count
        found = self.memory.find_translation("Test", "en", "es")
        self.assertEqual(found['usage_count'], 2)
    
    def test_user_dictionary(self):
        """Test user dictionary operations"""
        # Add term
        success = self.memory.add_to_user_dictionary(
            term="algorithm",
            translation="algoritmo",
            source_lang="en",
            target_lang="es"
        )
        
        self.assertTrue(success)
        
        # Retrieve term
        translation = self.memory.get_user_dictionary_term(
            term="algorithm",
            source_lang="en",
            target_lang="es"
        )
        
        self.assertEqual(translation, "algoritmo")
    
    def test_get_history(self):
        """Test retrieving translation history"""
        # Add multiple translations
        self.memory.add_translation("Hello", "Hola", "en", "es")
        self.memory.add_translation("Goodbye", "Adiós", "en", "es")
        
        # Get history
        history = self.memory.get_history(limit=10)
        
        self.assertGreaterEqual(len(history), 2)
    
    def test_statistics(self):
        """Test statistics retrieval"""
        # Add some translations
        self.memory.add_translation("Test1", "Prueba1", "en", "es", domain="technical")
        self.memory.add_translation("Test2", "Prueba2", "en", "es", domain="casual")
        
        # Get stats
        stats = self.memory.get_statistics()
        
        self.assertIn('total_translations', stats)
        self.assertGreaterEqual(stats['total_translations'], 2)
    
    def test_search_similar(self):
        """Test searching for similar translations"""
        # Add translations
        self.memory.add_translation("Hello world", "Hola mundo", "en", "es")
        self.memory.add_translation("Hello there", "Hola ahí", "en", "es")
        
        # Search
        results = self.memory.search_similar_translations("Hello", "en", "es", limit=5)
        
        self.assertGreater(len(results), 0)


if __name__ == '__main__':
    unittest.main()
