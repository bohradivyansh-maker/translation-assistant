"""
Context Analyzer Module
Performs NLP tasks: tokenization, NER, sentence segmentation, domain detection
Uses spaCy, NLTK, and scikit-learn for text analysis
"""

import logging
import re
from typing import List, Dict, Tuple, Optional
import json
import os

# NLP Libraries
import spacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)


class ContextAnalyzer:
    """
    Analyzes text context for better translation
    Includes: sentence segmentation, NER, domain detection, key term extraction
    """
    
    def __init__(self, spacy_model: str = 'en_core_web_sm'):
        """
        Initialize context analyzer
        
        Args:
            spacy_model: spaCy model to use (default: en_core_web_sm)
        """
        # Initialize spaCy
        try:
            self.nlp = spacy.load(spacy_model)
            logger.info(f"Loaded spaCy model: {spacy_model}")
        except Exception as e:
            logger.warning(f"Could not load {spacy_model}: {e}")
            logger.info("Creating blank English model")
            self.nlp = spacy.blank('en')
        
        # Initialize NLTK components
        self._initialize_nltk()
        
        # Initialize lemmatizer and stemmer
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        
        # Domain keywords (loaded from dictionary)
        self.domain_keywords = {
            'technical': ['algorithm', 'code', 'function', 'variable', 'database', 'API', 
                         'server', 'client', 'method', 'class', 'object', 'array', 'loop',
                         'iteration', 'compile', 'debug', 'syntax', 'parameter'],
            'casual': ['hello', 'hi', 'thanks', 'bye', 'please', 'sorry', 'yeah', 'okay',
                      'cool', 'awesome', 'great', 'nice', 'lol', 'omg'],
            'formal': ['pursuant', 'hereby', 'aforementioned', 'whereas', 'therefore',
                      'furthermore', 'nevertheless', 'accordingly', 'respective',
                      'subsequently', 'notwithstanding']
        }
        
        logger.info("Context analyzer initialized")
    
    def _initialize_nltk(self):
        """Download required NLTK data"""
        required_data = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                try:
                    nltk.download(data, quiet=True)
                except Exception as e:
                    logger.warning(f"Could not download NLTK data {data}: {e}")
        
        # Load stopwords
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.stop_words = set()
            logger.warning("Could not load stopwords")
    
    def segment_sentences(self, text: str) -> List[str]:
        """
        Segment text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        try:
            # Use spaCy for sentence segmentation
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents]
            
            if not sentences:
                # Fallback to NLTK
                sentences = sent_tokenize(text)
            
            return sentences
        except Exception as e:
            logger.error(f"Sentence segmentation error: {e}")
            # Simple fallback
            return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    def extract_context(
        self, 
        text: str, 
        selected_text: str,
        num_sentences_before: int = 2,
        num_sentences_after: int = 2
    ) -> Dict[str, str]:
        """
        Extract context around selected text
        
        Args:
            text: Full text
            selected_text: Selected portion to translate
            num_sentences_before: Number of sentences before to include
            num_sentences_after: Number of sentences after to include
            
        Returns:
            Dictionary with context_before, main_text, context_after
        """
        sentences = self.segment_sentences(text)
        
        # Find which sentence(s) contain the selected text
        selected_indices = []
        for idx, sent in enumerate(sentences):
            if selected_text.lower() in sent.lower():
                selected_indices.append(idx)
        
        if not selected_indices:
            return {
                'context_before': '',
                'main_text': selected_text,
                'context_after': ''
            }
        
        # Get range of sentences
        first_idx = selected_indices[0]
        last_idx = selected_indices[-1]
        
        start_idx = max(0, first_idx - num_sentences_before)
        end_idx = min(len(sentences), last_idx + num_sentences_after + 1)
        
        context_before = ' '.join(sentences[start_idx:first_idx])
        main_text = ' '.join(sentences[first_idx:last_idx + 1])
        context_after = ' '.join(sentences[last_idx + 1:end_idx])
        
        return {
            'context_before': context_before,
            'main_text': main_text,
            'context_after': context_after
        }
    
    def extract_named_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities using spaCy NER
        
        Args:
            text: Input text
            
        Returns:
            List of dictionaries with entity text, label, and position
        """
        try:
            doc = self.nlp(text)
            entities = []
            
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            
            return entities
        except Exception as e:
            logger.error(f"NER extraction error: {e}")
            return []
    
    def get_entity_texts(self, text: str) -> List[str]:
        """
        Get list of entity texts to preserve during translation
        
        Args:
            text: Input text
            
        Returns:
            List of entity strings
        """
        entities = self.extract_named_entities(text)
        # Filter for important entity types
        important_types = ['PERSON', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT']
        return [ent['text'] for ent in entities if ent['label'] in important_types]
    
    def tokenize_and_preprocess(self, text: str) -> Dict[str, any]:
        """
        Comprehensive text preprocessing
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with various tokenization and preprocessing results
        """
        # Word tokenization
        words = word_tokenize(text.lower())
        
        # Remove stopwords
        filtered_words = [w for w in words if w not in self.stop_words and w.isalnum()]
        
        # Lemmatization
        lemmatized = [self.lemmatizer.lemmatize(w) for w in filtered_words]
        
        # Stemming
        stemmed = [self.stemmer.stem(w) for w in filtered_words]
        
        return {
            'original_tokens': words,
            'filtered_tokens': filtered_words,
            'lemmatized': lemmatized,
            'stemmed': stemmed,
            'num_tokens': len(words),
            'num_unique_tokens': len(set(words))
        }
    
    def detect_domain(self, text: str) -> Dict[str, float]:
        """
        Detect text domain (technical/casual/formal) using keyword matching
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with domain scores
        """
        text_lower = text.lower()
        words = set(word_tokenize(text_lower))
        
        scores = {}
        for domain, keywords in self.domain_keywords.items():
            matching_keywords = words.intersection(set(keywords))
            score = len(matching_keywords) / len(keywords) if keywords else 0
            scores[domain] = score
        
        return scores
    
    def get_primary_domain(self, text: str) -> str:
        """
        Get primary domain classification
        
        Args:
            text: Input text
            
        Returns:
            Domain name (technical/casual/formal/general)
        """
        scores = self.detect_domain(text)
        
        if not scores or max(scores.values()) == 0:
            return 'general'
        
        return max(scores, key=scores.get)
    
    def extract_key_terms(self, text: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Extract key terms using TF-IDF
        
        Args:
            text: Input text
            top_n: Number of top terms to return
            
        Returns:
            List of (term, score) tuples
        """
        try:
            # Need at least 2 documents for TF-IDF
            sentences = self.segment_sentences(text)
            
            if len(sentences) < 2:
                # Fallback: return most frequent non-stopword tokens
                tokens = self.tokenize_and_preprocess(text)
                word_freq = {}
                for word in tokens['filtered_tokens']:
                    word_freq[word] = word_freq.get(word, 0) + 1
                sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
                return sorted_words[:top_n]
            
            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Get feature names and scores
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.sum(axis=0).A1
            
            term_scores = list(zip(feature_names, scores))
            term_scores.sort(key=lambda x: x[1], reverse=True)
            
            return term_scores[:top_n]
            
        except Exception as e:
            logger.error(f"Key term extraction error: {e}")
            return []
    
    def analyze_full_context(self, text: str, selected_text: Optional[str] = None) -> Dict[str, any]:
        """
        Perform complete context analysis
        
        Args:
            text: Full text to analyze
            selected_text: Optional selected portion
            
        Returns:
            Comprehensive analysis dictionary
        """
        # Extract context if selected text provided
        if selected_text:
            context = self.extract_context(text, selected_text)
        else:
            context = {
                'context_before': '',
                'main_text': text,
                'context_after': ''
            }
        
        # Named entities
        entities = self.extract_named_entities(text)
        entity_texts = self.get_entity_texts(text)
        
        # Preprocessing
        preprocessing = self.tokenize_and_preprocess(text)
        
        # Domain detection
        domain_scores = self.detect_domain(text)
        primary_domain = self.get_primary_domain(text)
        
        # Key terms
        key_terms = self.extract_key_terms(text)
        
        # Sentence segmentation
        sentences = self.segment_sentences(text)
        
        return {
            'context': context,
            'entities': entities,
            'entity_texts': entity_texts,
            'preprocessing': preprocessing,
            'domain_scores': domain_scores,
            'primary_domain': primary_domain,
            'key_terms': key_terms,
            'sentences': sentences,
            'num_sentences': len(sentences)
        }


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize analyzer
    analyzer = ContextAnalyzer()
    
    # Test text
    test_text = """
    John Smith is a software engineer at Google. He works on machine learning algorithms.
    The algorithm converges after 100 iterations. It uses gradient descent optimization.
    This is a breakthrough in artificial intelligence research.
    """
    
    print("=== Full Context Analysis ===")
    analysis = analyzer.analyze_full_context(test_text)
    
    print(f"\nSentences: {len(analysis['sentences'])}")
    print(f"Primary Domain: {analysis['primary_domain']}")
    print(f"Domain Scores: {analysis['domain_scores']}")
    print(f"\nNamed Entities: {len(analysis['entities'])}")
    for ent in analysis['entities']:
        print(f"  - {ent['text']} ({ent['label']})")
    
    print(f"\nKey Terms:")
    for term, score in analysis['key_terms']:
        print(f"  - {term}: {score:.3f}")
    
    print(f"\nEntity texts to preserve: {analysis['entity_texts']}")
    
    # Test context extraction
    print("\n=== Context Extraction ===")
    selected = "The algorithm converges after 100 iterations."
    context = analyzer.extract_context(test_text, selected)
    print(f"Before: {context['context_before']}")
    print(f"Main: {context['main_text']}")
    print(f"After: {context['context_after']}")
