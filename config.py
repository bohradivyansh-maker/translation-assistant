# Configuration file for Translation Assistant

# Application settings
APP_NAME = "Context-Aware Translation Assistant"
APP_VERSION = "1.0.0"

# Default settings
DEFAULT_TARGET_LANGUAGE = "es"
DEFAULT_CONTEXT_SENTENCES = 2
MAX_TRANSLATION_LENGTH = 5000

# Hotkey configuration
HOTKEY_COMBINATION = "ctrl+shift+t"

# Database settings
DATABASE_PATH = "data/translation_memory.db"
CUSTOM_DICTIONARY_PATH = "data/custom_dictionary.json"

# Audio settings
AUDIO_CACHE_DIR = "temp/audio"
AUDIO_CACHE_MAX_AGE_HOURS = 24

# GUI settings
POPUP_WIDTH = 500
POPUP_MIN_HEIGHT = 200
POPUP_OFFSET_X = 20
POPUP_OFFSET_Y = 20

# Translation settings
TRANSLATION_TIMEOUT = 10  # seconds
TRANSLATION_RETRY_ATTEMPTS = 3
PRESERVE_ENTITY_TYPES = ["PERSON", "ORG", "GPE", "LOC", "PRODUCT", "EVENT"]

# NLP settings
SPACY_MODEL = "en_core_web_sm"
TF_IDF_MAX_FEATURES = 10
KEY_TERMS_COUNT = 5

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = "translation_assistant.log"
LOG_MAX_SIZE_MB = 10
LOG_BACKUP_COUNT = 3

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'zh-cn': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'ko': 'Korean'
}

# Domain keywords
TECHNICAL_KEYWORDS = [
    'algorithm', 'code', 'function', 'variable', 'database', 'API',
    'server', 'client', 'method', 'class', 'object', 'array', 'loop',
    'iteration', 'compile', 'debug', 'syntax', 'parameter', 'framework',
    'library', 'module', 'import', 'export', 'interface', 'protocol'
]

CASUAL_KEYWORDS = [
    'hello', 'hi', 'hey', 'thanks', 'thank you', 'bye', 'goodbye',
    'please', 'sorry', 'yeah', 'yes', 'no', 'okay', 'ok', 'cool',
    'awesome', 'great', 'nice', 'good', 'bad', 'lol', 'omg'
]

FORMAL_KEYWORDS = [
    'pursuant', 'hereby', 'aforementioned', 'whereas', 'therefore',
    'furthermore', 'nevertheless', 'accordingly', 'respective',
    'subsequently', 'notwithstanding', 'henceforth', 'herein',
    'hereinafter', 'undersigned', 'aforesaid', 'therein', 'thereof'
]
