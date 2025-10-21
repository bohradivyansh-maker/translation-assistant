"""
Context-Aware Translation Assistant
Main Application Entry Point

NLP Mini Project
Demonstrates: Translation, NER, Context Analysis, Domain Detection, TTS
"""

import logging
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.translator import TranslationEngine
from src.context_analyzer import ContextAnalyzer
from src.hotkey_handler import HotkeyHandler
from src.gui import TranslationPopup
from src.memory import TranslationMemory
from src.audio_handler import AudioHandler
from src.language_selector import LanguageSelector
from src.system_tray import SystemTrayIcon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('translation_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TranslationAssistant:
    """
    Main application class integrating all components
    """
    
    def __init__(self, target_language: str = 'es'):
        """
        Initialize the translation assistant
        
        Args:
            target_language: Default target language for translations
        """
        logger.info("Initializing Translation Assistant...")
        
        # Configuration
        self.target_language = target_language
        self.data_dir = Path(__file__).parent / 'data'
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize components
        try:
            # Translation engine
            custom_dict_path = self.data_dir / 'custom_dictionary.json'
            self.translator = TranslationEngine(str(custom_dict_path))
            
            # Context analyzer
            self.analyzer = ContextAnalyzer()
            
            # Translation memory
            memory_path = self.data_dir / 'translation_memory.db'
            self.memory = TranslationMemory(str(memory_path))
            
            # Audio handler
            self.audio = AudioHandler()
            
            # GUI popup
            self.popup = TranslationPopup(
                on_copy=self._handle_copy,
                on_speak=self._handle_speak,
                on_save=self._handle_save
            )
            
            # Hotkey handler (initialized last)
            self.hotkey_handler = HotkeyHandler(hotkey_callback=self._handle_hotkey)
            
            # System tray (for easy exit)
            self.system_tray = SystemTrayIcon(on_exit_callback=self.stop)
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise
    
    def _handle_hotkey(self, selected_text: str, cursor_position: tuple):
        """
        Handle hotkey trigger event
        
        Args:
            selected_text: Text selected by user
            cursor_position: Cursor position for popup placement
        """
        try:
            if not selected_text or selected_text.strip() == "":
                logger.warning("No text selected")
                return
            
            logger.info(f"Processing translation request for: {selected_text[:50]}...")
            
            # Show language selector first
            selector = LanguageSelector(self.target_language)
            
            # Store data for translation after selection
            self._pending_translation = {
                'text': selected_text,
                'position': cursor_position
            }
            
            # Show selector and wait for language choice
            selector.show(cursor_position, callback=lambda lang: self._perform_translation(lang))
            
        except Exception as e:
            logger.error(f"Error handling hotkey: {e}", exc_info=True)
    
    def _perform_translation(self, target_lang: str):
        """
        Perform the actual translation after language selection
        
        Args:
            target_lang: Selected target language
        """
        try:
            if not hasattr(self, '_pending_translation'):
                return
            
            selected_text = self._pending_translation['text']
            cursor_position = self._pending_translation['position']
            
            # Step 1: Perform context analysis
            analysis = self.analyzer.analyze_full_context(selected_text)
            
            logger.info(f"Context analysis complete:")
            logger.info(f"  - Domain: {analysis['primary_domain']}")
            logger.info(f"  - Entities found: {len(analysis['entities'])}")
            logger.info(f"  - Key terms: {[t[0] for t in analysis['key_terms'][:3]]}")
            
            # Step 2: Check translation memory
            detected_lang, confidence = self.translator.detect_language(selected_text)
            cached_translation = self.memory.find_translation(
                selected_text,
                detected_lang,
                target_lang
            )
            
            if cached_translation:
                logger.info("Found cached translation")
                translation_result = {
                    'original_text': selected_text,
                    'translated_text': cached_translation['translated_text'],
                    'source_language': cached_translation['source_lang'],
                    'target_language': cached_translation['target_lang'],
                    'confidence': cached_translation['confidence'],
                    'method': 'cache'
                }
            else:
                # Step 3: Perform translation WITHOUT entity preservation
                # (Entity preservation was causing mixed language output)
                # Only preserve proper nouns like names and places if needed
                
                translation_result = self.translator.translate(
                    selected_text,
                    target_lang=target_lang,
                    preserve_entities=None  # Disabled for cleaner translations
                )
                
                # Step 4: Store in translation memory
                self.memory.add_translation(
                    original_text=selected_text,
                    translated_text=translation_result['translated_text'],
                    source_lang=translation_result['source_language'],
                    target_lang=translation_result['target_language'],
                    context=analysis['context']['context_before'],
                    domain=analysis['primary_domain'],
                    entities=[],  # No entities preserved
                    confidence=translation_result['confidence'],
                    method=translation_result['method']
                )
                
                logger.info("Translation stored in memory")
            
            # Step 5: Display popup with results
            metadata = {
                'domain': analysis['primary_domain'],
                'confidence': translation_result['confidence'],
                'entities': [],  # No entities preserved for cleaner output
                'method': translation_result.get('method', 'unknown')
            }
            
            self.popup.show(
                original_text=selected_text,
                translated_text=translation_result['translated_text'],
                source_lang=translation_result['source_language'],
                target_lang=translation_result['target_language'],
                position=cursor_position,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error handling hotkey: {e}", exc_info=True)
    
    def _handle_copy(self, text: str):
        """Handle copy button click"""
        logger.info("Copy action executed")
    
    def _handle_speak(self, text: str, lang: str):
        """Handle speak button click"""
        try:
            logger.info(f"Speaking text in {lang}")
            self.audio.speak(text, lang, blocking=False)
        except Exception as e:
            logger.error(f"Error in speak handler: {e}")
    
    def _handle_save(self, original: str, translation: str, source_lang: str, target_lang: str):
        """Handle save to dictionary button click"""
        try:
            logger.info("Saving to user dictionary")
            self.memory.add_to_user_dictionary(
                term=original,
                translation=translation,
                source_lang=source_lang,
                target_lang=target_lang
            )
        except Exception as e:
            logger.error(f"Error in save handler: {e}")
    
    def set_target_language(self, lang_code: str):
        """Change target language"""
        if self.translator.is_language_supported(lang_code):
            self.target_language = lang_code
            logger.info(f"Target language changed to: {lang_code}")
        else:
            logger.warning(f"Language not supported: {lang_code}")
    
    def get_statistics(self):
        """Get usage statistics"""
        return self.memory.get_statistics()
    
    def start(self):
        """Start the application"""
        try:
            logger.info("="*60)
            logger.info("Context-Aware Translation Assistant Started")
            logger.info("="*60)
            logger.info(f"Target Language: {self.target_language}")
            logger.info(f"Hotkey: Ctrl+Shift+T")
            logger.info("Select text in any application and press the hotkey to translate")
            logger.info("="*60)
            
            # Start hotkey listener
            self.hotkey_handler.start()
            
            # Keep application running with status window
            print("\n" + "="*60)
            print("🌐 TRANSLATION ASSISTANT RUNNING")
            print("="*60)
            print(f"Target Language: {self.target_language.upper()}")
            print("\nKEYBOARD SHORTCUTS:")
            print("  • Ctrl+Shift+T  - Translate selected text")
            print("  • Ctrl+Shift+Q  - Exit application")
            print("\nA status window will appear in the bottom-right corner.")
            print("You can minimize it - the app keeps running in background.")
            print("="*60 + "\n")
            
            # Run system tray (this will block until exit)
            self.system_tray.run()
                
        except Exception as e:
            logger.error(f"Error starting application: {e}")
            raise
    
    def stop(self):
        """Stop the application"""
        logger.info("Stopping Translation Assistant...")
        
        try:
            # Stop hotkey listener
            self.hotkey_handler.stop()
            
            # Close database connection
            self.memory.close()
            
            # Show statistics
            stats = self.get_statistics()
            logger.info("Session Statistics:")
            logger.info(f"  Total translations: {stats.get('total_translations', 0)}")
            logger.info(f"  Total usage: {stats.get('total_usage', 0)}")
            
            logger.info("Translation Assistant stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping application: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Context-Aware Translation Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --lang es          # Translate to Spanish
  python main.py --lang fr          # Translate to French
  python main.py --lang hi          # Translate to Hindi

Supported languages:
  en (English), es (Spanish), fr (French), de (German),
  hi (Hindi), it (Italian), pt (Portuguese), ru (Russian),
  ja (Japanese), zh-cn (Chinese), ar (Arabic), ko (Korean)
        """
    )
    
    parser.add_argument(
        '--lang',
        type=str,
        default='en',
        help='Default target language code (default: en for English)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create and start application
    try:
        app = TranslationAssistant(target_language=args.lang)
        app.start()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
