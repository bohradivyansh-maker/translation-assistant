"""
Audio Handler Module
Manages text-to-speech functionality using gTTS
Provides pronunciation playback for translations
"""

import logging
import os
import tempfile
import threading
import time
from typing import Optional

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logging.warning("gTTS not installed. Text-to-speech will not work. Install with: pip install gTTS")

try:
    # Try playsound3 first (recommended for Python 3.9+)
    from playsound3 import playsound
    PLAYSOUND_AVAILABLE = True
    AUDIO_METHOD = "playsound3"
except ImportError:
    # pygame removed due to Python 3.12+ compatibility (distutils removed)
    # If playsound3 is not available, audio will be disabled
    PLAYSOUND_AVAILABLE = False
    AUDIO_METHOD = "none"
    logging.warning("playsound3 not installed. Audio playback disabled. Install with: pip install playsound3")

logger = logging.getLogger(__name__)


class AudioHandler:
    """
    Handles text-to-speech audio generation and playback
    """
    
    # Supported TTS languages
    SUPPORTED_TTS_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ko': 'Korean'
    }
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize audio handler
        
        Args:
            cache_dir: Directory to cache audio files (default: temp)
        """
        self.cache_dir = cache_dir or tempfile.gettempdir()
        self.current_playback = None
        self.is_playing = False
        
        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)
        
        logger.info("Audio handler initialized")
    
    def generate_audio(
        self,
        text: str,
        lang: str = 'en',
        slow: bool = False
    ) -> Optional[str]:
        """
        Generate audio file from text
        
        Args:
            text: Text to convert to speech
            lang: Language code
            slow: Use slow speech rate
            
        Returns:
            Path to generated audio file or None
        """
        if not GTTS_AVAILABLE:
            logger.error("gTTS not installed. Cannot generate audio.")
            return None
            
        try:
            # Validate language
            if lang not in self.SUPPORTED_TTS_LANGUAGES:
                logger.warning(f"Language {lang} not supported, using English")
                lang = 'en'
            
            # Create temporary file
            filename = f"tts_{hash(text)}_{lang}.mp3"
            filepath = os.path.join(self.cache_dir, filename)
            
            # Check if already cached
            if os.path.exists(filepath):
                logger.info(f"Using cached audio: {filepath}")
                return filepath
            
            # Generate TTS
            logger.info(f"Generating TTS for: {text[:50]}... (lang: {lang})")
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(filepath)
            
            logger.info(f"Audio generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return None
    
    def play_audio(self, filepath: str, blocking: bool = False):
        """
        Play audio file
        
        Args:
            filepath: Path to audio file
            blocking: Wait for playback to finish
        """
        if not PLAYSOUND_AVAILABLE:
            logger.error("No audio playback library available. Cannot play audio.")
            return
            
        try:
            if not os.path.exists(filepath):
                logger.error(f"Audio file not found: {filepath}")
                return
            
            logger.info(f"Playing audio: {filepath}")
            
            if blocking:
                playsound(filepath)
            else:
                # Play in separate thread
                playback_thread = threading.Thread(
                    target=playsound,
                    args=(filepath,),
                    daemon=True
                )
                playback_thread.start()
                self.current_playback = playback_thread
            
            self.is_playing = True
            
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            self.is_playing = False
    
    def speak(
        self,
        text: str,
        lang: str = 'en',
        slow: bool = False,
        blocking: bool = False
    ) -> bool:
        """
        Generate and play text-to-speech
        
        Args:
            text: Text to speak
            lang: Language code
            slow: Use slow speech rate
            blocking: Wait for playback to finish
            
        Returns:
            True if successful
        """
        try:
            # Generate audio
            filepath = self.generate_audio(text, lang, slow)
            
            if not filepath:
                return False
            
            # Play audio
            self.play_audio(filepath, blocking)
            return True
            
        except Exception as e:
            logger.error(f"Error in speak: {e}")
            return False
    
    def speak_translation(
        self,
        original_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        play_both: bool = False
    ):
        """
        Speak translation (and optionally original)
        
        Args:
            original_text: Original text
            translated_text: Translated text
            source_lang: Source language
            target_lang: Target language
            play_both: Play both original and translation
        """
        try:
            if play_both:
                # Play original
                logger.info("Playing original text...")
                self.speak(original_text, source_lang, blocking=True)
                
                # Small pause
                time.sleep(0.5)
            
            # Play translation
            logger.info("Playing translation...")
            self.speak(translated_text, target_lang, blocking=False)
            
        except Exception as e:
            logger.error(f"Error speaking translation: {e}")
    
    def stop_playback(self):
        """Stop current playback"""
        # Note: playsound doesn't support stopping, this is a limitation
        # In production, consider using pygame or pydub for better control
        self.is_playing = False
        logger.info("Playback stop requested (limited support)")
    
    def clear_cache(self, max_age_hours: Optional[int] = None):
        """
        Clear cached audio files
        
        Args:
            max_age_hours: Only delete files older than this (None = all)
        """
        try:
            deleted_count = 0
            current_time = time.time()
            
            for filename in os.listdir(self.cache_dir):
                if filename.startswith("tts_") and filename.endswith(".mp3"):
                    filepath = os.path.join(self.cache_dir, filename)
                    
                    if max_age_hours:
                        file_age_hours = (current_time - os.path.getmtime(filepath)) / 3600
                        if file_age_hours < max_age_hours:
                            continue
                    
                    os.remove(filepath)
                    deleted_count += 1
            
            logger.info(f"Cleared {deleted_count} cached audio files")
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def get_supported_languages(self) -> dict:
        """Get dictionary of supported TTS languages"""
        return self.SUPPORTED_TTS_LANGUAGES.copy()
    
    def is_language_supported(self, lang_code: str) -> bool:
        """Check if language is supported for TTS"""
        return lang_code in self.SUPPORTED_TTS_LANGUAGES


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize handler
    audio_handler = AudioHandler()
    
    print("=== Audio Handler Test ===\n")
    
    # Test 1: Simple TTS
    print("Test 1: Speaking English...")
    success = audio_handler.speak("Hello, this is a test of the text to speech system.", lang='en')
    print(f"Success: {success}\n")
    
    time.sleep(3)
    
    # Test 2: Spanish TTS
    print("Test 2: Speaking Spanish...")
    success = audio_handler.speak("Hola, ¿cómo estás?", lang='es')
    print(f"Success: {success}\n")
    
    time.sleep(3)
    
    # Test 3: Translation pronunciation
    print("Test 3: Translation pronunciation...")
    audio_handler.speak_translation(
        original_text="Good morning",
        translated_text="Buenos días",
        source_lang='en',
        target_lang='es',
        play_both=True
    )
    
    time.sleep(5)
    
    # Test 4: Supported languages
    print("\nSupported languages:")
    for code, name in audio_handler.get_supported_languages().items():
        print(f"  {code}: {name}")
    
    print("\nTest complete!")
