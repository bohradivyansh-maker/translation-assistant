"""
Unit tests for Context Analyzer
"""

import unittest
from src.context_analyzer import ContextAnalyzer


class TestContextAnalyzer(unittest.TestCase):
    """Test cases for context analyzer"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize analyzer once for all tests"""
        cls.analyzer = ContextAnalyzer()
    
    def test_sentence_segmentation(self):
        """Test sentence segmentation"""
        text = "Hello there. How are you? I am fine."
        sentences = self.analyzer.segment_sentences(text)
        
        self.assertEqual(len(sentences), 3)
        self.assertIn("Hello there", sentences[0])
    
    def test_entity_extraction(self):
        """Test named entity recognition"""
        text = "John Smith works at Microsoft in Seattle."
        entities = self.analyzer.extract_named_entities(text)
        
        # Should find at least the person name and organization
        self.assertGreater(len(entities), 0)
        
        # Check entity structure
        if entities:
            entity = entities[0]
            self.assertIn('text', entity)
            self.assertIn('label', entity)
    
    def test_entity_texts_extraction(self):
        """Test extracting entity texts for preservation"""
        text = "John Smith works at Microsoft."
        entity_texts = self.analyzer.get_entity_texts(text)
        
        # Should find relevant entities
        self.assertIsInstance(entity_texts, list)
    
    def test_context_extraction(self):
        """Test context extraction around selected text"""
        full_text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        selected = "Second sentence"
        
        context = self.analyzer.extract_context(full_text, selected, 1, 1)
        
        self.assertIn('context_before', context)
        self.assertIn('main_text', context)
        self.assertIn('context_after', context)
    
    def test_tokenization(self):
        """Test tokenization and preprocessing"""
        text = "The quick brown fox jumps."
        result = self.analyzer.tokenize_and_preprocess(text)
        
        self.assertIn('original_tokens', result)
        self.assertIn('filtered_tokens', result)
        self.assertIn('lemmatized', result)
        self.assertIn('stemmed', result)
        self.assertGreater(result['num_tokens'], 0)
    
    def test_domain_detection(self):
        """Test domain classification"""
        technical_text = "The algorithm iterates through the array using a loop."
        casual_text = "Hey there! How are you doing today?"
        formal_text = "Pursuant to the aforementioned agreement, we hereby submit."
        
        tech_scores = self.analyzer.detect_domain(technical_text)
        casual_scores = self.analyzer.detect_domain(casual_text)
        formal_scores = self.analyzer.detect_domain(formal_text)
        
        # Technical text should score higher on technical
        self.assertGreater(tech_scores['technical'], tech_scores['casual'])
        
        # Casual text should score higher on casual
        self.assertGreater(casual_scores['casual'], casual_scores['formal'])
    
    def test_primary_domain(self):
        """Test primary domain identification"""
        technical_text = "The function returns an array of objects."
        domain = self.analyzer.get_primary_domain(technical_text)
        
        self.assertIn(domain, ['technical', 'casual', 'formal', 'general'])
    
    def test_key_term_extraction(self):
        """Test key term extraction"""
        text = "Machine learning algorithms process data efficiently."
        key_terms = self.analyzer.extract_key_terms(text, top_n=3)
        
        self.assertIsInstance(key_terms, list)
        self.assertLessEqual(len(key_terms), 3)
    
    def test_full_context_analysis(self):
        """Test comprehensive context analysis"""
        text = "John Smith is a software engineer. He works on AI algorithms."
        analysis = self.analyzer.analyze_full_context(text)
        
        # Check all expected keys
        self.assertIn('context', analysis)
        self.assertIn('entities', analysis)
        self.assertIn('preprocessing', analysis)
        self.assertIn('domain_scores', analysis)
        self.assertIn('primary_domain', analysis)
        self.assertIn('key_terms', analysis)
        self.assertIn('sentences', analysis)


if __name__ == '__main__':
    unittest.main()
