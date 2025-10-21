"""
Core Translation Module
Handles translation using Google Translate API with fallback to deep-translator
Includes language detection and multi-language support
"""

import logging
from typing import Optional, Dict, Tuple

# Try importing googletrans (fails on Python 3.13+ due to missing 'cgi' module)
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    GOOGLETRANS_AVAILABLE = False
    logging.warning(f"googletrans not available: {e}. Using deep-translator as primary.")

from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import json
import os

# Set seed for consistent language detection
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)


class TranslationEngine:
    """
    Main translation engine with context-aware capabilities
    """
    
    # Supported languages mapping
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'zh-cn': 'Chinese (Simplified)',
        'ar': 'Arabic',
        'ko': 'Korean'
    }
    
    def __init__(self, custom_dict_path: Optional[str] = None):
        """
        Initialize translation engine
        
        Args:
            custom_dict_path: Path to custom dictionary JSON file
        """
        # Initialize googletrans only if available (Python 3.12 and below)
        self.translator = Translator() if GOOGLETRANS_AVAILABLE else None
        self.use_deep_translator = not GOOGLETRANS_AVAILABLE
        self.custom_dict = {}
        
        if custom_dict_path and os.path.exists(custom_dict_path):
            self._load_custom_dictionary(custom_dict_path)
        
        translator_type = "googletrans" if GOOGLETRANS_AVAILABLE else "deep-translator (primary)"
        logger.info(f"Translation engine initialized using {translator_type}")
    
    def _load_custom_dictionary(self, dict_path: str):
        """Load custom terminology dictionary"""
        try:
            with open(dict_path, 'r', encoding='utf-8') as f:
                self.custom_dict = json.load(f)
            logger.info(f"Loaded custom dictionary from {dict_path}")
        except Exception as e:
            logger.error(f"Error loading custom dictionary: {e}")
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            # Try with googletrans if available
            if GOOGLETRANS_AVAILABLE and self.translator:
                detected = self.translator.detect(text)
                return detected.lang, detected.confidence
            else:
                # Use langdetect as primary on Python 3.13+
                lang = detect(text)
                return lang, 0.99  # langdetect doesn't provide confidence
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            try:
                # Fallback to langdetect
                lang = detect(text)
                return lang, 0.95
            except Exception as e2:
                logger.error(f"Language detection failed: {e2}")
                return 'en', 0.5
    
    def translate(
        self, 
        text: str, 
        target_lang: str = 'en',
        source_lang: Optional[str] = None,
        preserve_entities: Optional[list] = None
    ) -> Dict[str, any]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (default: 'en')
            source_lang: Source language code (auto-detect if None)
            preserve_entities: List of entities to preserve during translation
            
        Returns:
            Dictionary containing translation results
        """
        try:
            # Detect source language if not provided
            if source_lang is None:
                source_lang, confidence = self.detect_language(text)
                logger.info(f"Detected language: {source_lang} (confidence: {confidence})")
            else:
                confidence = 1.0
            
            # Don't translate if source and target are the same
            if source_lang == target_lang:
                return {
                    'original_text': text,
                    'translated_text': text,
                    'source_language': source_lang,
                    'target_language': target_lang,
                    'confidence': confidence,
                    'method': 'no_translation_needed'
                }
            
            # Replace entities with placeholders if provided
            entity_map = {}
            working_text = text
            if preserve_entities:
                for idx, entity in enumerate(preserve_entities):
                    placeholder = f"__ENTITY_{idx}__"
                    entity_map[placeholder] = entity
                    working_text = working_text.replace(entity, placeholder)
            
            # Attempt translation
            try:
                # Use googletrans if available (Python 3.12 and below)
                if GOOGLETRANS_AVAILABLE and self.translator:
                    translation = self.translator.translate(
                        working_text,
                        src=source_lang,
                        dest=target_lang
                    )
                    translated_text = translation.text
                    method = 'googletrans'
                else:
                    # Use deep-translator as primary (Python 3.13+)
                    translator = GoogleTranslator(source=source_lang, target=target_lang)
                    translated_text = translator.translate(working_text)
                    method = 'deep_translator'
            except Exception as e:
                logger.warning(f"Primary translator failed: {e}, trying fallback")
                # Fallback to deep-translator
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                translated_text = translator.translate(working_text)
                method = 'deep_translator_fallback'
            
            # Restore entities
            for placeholder, entity in entity_map.items():
                translated_text = translated_text.replace(placeholder, entity)
            
            return {
                'original_text': text,
                'translated_text': translated_text,
                'source_language': source_lang,
                'target_language': target_lang,
                'confidence': confidence,
                'method': method,
                'preserved_entities': list(entity_map.values()) if entity_map else []
            }
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return {
                'original_text': text,
                'translated_text': text,
                'source_language': source_lang or 'unknown',
                'target_language': target_lang,
                'confidence': 0.0,
                'method': 'error',
                'error': str(e)
            }
    
    def translate_with_context(
        self,
        text: str,
        context_before: str = "",
        context_after: str = "",
        target_lang: str = 'en',
        preserve_entities: Optional[list] = None
    ) -> Dict[str, any]:
        """
        Translate text with surrounding context for better accuracy
        
        Args:
            text: Main text to translate
            context_before: Previous context (sentences before)
            context_after: Following context (sentences after)
            target_lang: Target language code
            preserve_entities: List of entities to preserve
            
        Returns:
            Translation result dictionary
        """
        # Build full context
        full_context = f"{context_before} {text} {context_after}".strip()
        
        # Translate with full context
        result = self.translate(
            full_context,
            target_lang=target_lang,
            preserve_entities=preserve_entities
        )
        
        # Try to extract just the main translation
        # This is a simple heuristic - in production, use better alignment
        if result['method'] != 'error':
            words_before = len(context_before.split())
            words_main = len(text.split())
            translated_words = result['translated_text'].split()
            
            # Extract approximate translated portion
            if len(translated_words) > words_main:
                start_idx = max(0, words_before)
                end_idx = min(len(translated_words), start_idx + words_main + 5)
                main_translation = ' '.join(translated_words[start_idx:end_idx])
            else:
                main_translation = result['translated_text']
            
            result['translated_text'] = main_translation
            result['context_used'] = True
        
        return result
    
    def batch_translate(
        self,
        texts: list,
        target_lang: str = 'en',
        source_lang: Optional[str] = None
    ) -> list:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            source_lang: Source language code
            
        Returns:
            List of translation result dictionaries
        """
        results = []
        for text in texts:
            result = self.translate(text, target_lang, source_lang)
            results.append(result)
        return results
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported languages"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def is_language_supported(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.SUPPORTED_LANGUAGES


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize translator
    translator = TranslationEngine()
    
    # Test 1: Simple translation
    print("\n=== Test 1: Simple Translation ===")
    result = translator.translate("Hello, how are you?", target_lang='es')
    print(f"Original: {result['original_text']}")
    print(f"Translated: {result['translated_text']}")
    print(f"Language: {result['source_language']} -> {result['target_language']}")
    
    # Test 2: Language detection
    print("\n=== Test 2: Language Detection ===")
    text = "Bonjour, comment allez-vous?"
    lang, conf = translator.detect_language(text)
    print(f"Text: {text}")
    print(f"Detected: {lang} (confidence: {conf})")
    
    # Test 3: Entity preservation
    print("\n=== Test 3: Entity Preservation ===")
    result = translator.translate(
        "John Smith works at Microsoft",
        target_lang='es',
        preserve_entities=['John Smith', 'Microsoft']
    )
    print(f"Original: {result['original_text']}")
    print(f"Translated: {result['translated_text']}")
    print(f"Preserved: {result.get('preserved_entities', [])}")
    
    # Test 4: Context-aware translation
    print("\n=== Test 4: Context-Aware Translation ===")
    result = translator.translate_with_context(
        text="It was a great time.",
        context_before="I went to the concert yesterday.",
        target_lang='es'
    )
    print(f"Original: {result['original_text']}")
    print(f"Translated: {result['translated_text']}")
    print(f"Context used: {result.get('context_used', False)}")
