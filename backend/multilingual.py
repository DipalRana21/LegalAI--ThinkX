"""
Multilingual Support Module
Handles speech-to-text, text-to-speech, and translation for Indian languages
"""

import os
import sys
import tempfile
import logging
from typing import Optional, Dict, List, Tuple
from enum import Enum
from functools import lru_cache

# Setup logging
logger = logging.getLogger(__name__)

# Try alternative translation methods
translator_available = False
Translator = None
LANGUAGES = {}

# Try MyMemory API (free, no key needed)
try:
    import requests
    requests_available = True
    translator_available = True
    logger.info("✓ Using MyMemory Translation API (Free)")
except ImportError:
    requests_available = False
    logger.warning("requests library not available - translation limited to dictionary")

# Fallback: Dictionary-based translation for common legal terms
BASIC_TRANSLATIONS = {
    'en_hi': {
        'what': 'क्या', 'is': 'है', 'the': 'यह', 'punishment': 'सजा',
        'for': 'के लिए', 'theft': 'चोरी', 'bail': 'जमानत', 'section': 'धारा',
        'court': 'अदालत', 'law': 'कानून', 'crime': 'अपराध', 'offense': 'अपराध',
        'arrest': 'गिरफ्तारी', 'fine': 'जुर्माना', 'imprisonment': 'कारावास',
    },
    'en_bn': {
        'what': 'কি', 'is': 'হয়', 'the': 'এই', 'punishment': 'শাস্তি',
        'for': 'জন্য', 'theft': 'চুরি', 'bail': 'জামিন', 'section': 'ধারা',
        'court': 'আদালত', 'law': 'আইন', 'crime': 'অপরাধ', 'offense': 'অপরাধ',
    },
    'en_ta': {
        'what': 'என்ன', 'is': 'இருக்கிறது', 'the': 'இந்த', 'punishment': 'தண்டனை',
        'for': 'க்கு', 'theft': 'திருட்டு', 'bail': 'பிணை', 'section': 'பிரிவு',
        'court': 'நீதிமன்றம்', 'law': 'சட்டம்', 'crime': 'குற்றம்',
    },
}


class LanguageCode(Enum):
    """Standard language codes for Indian languages"""
    ENGLISH = "en"
    HINDI = "hi"
    BENGALI = "bn"
    TELUGU = "te"
    MARATHI = "mr"
    TAMIL = "ta"
    KANNADA = "kn"
    GUJARATI = "gu"
    MALAYALAM = "ml"
    PUNJABI = "pa"
    URDU = "ur"
    ODIA = "or"


# Supported Indian languages for voice input and output
INDIAN_LANGUAGES = {
    'english': {
        'code': LanguageCode.ENGLISH.value,
        'name': 'English',
        'native_name': 'English',
        'voice_code': 'en-IN',
        'flag': '🇬🇧',
        'is_rtl': False,
        'supported': True
    },
    'hindi': {
        'code': LanguageCode.HINDI.value,
        'name': 'हिन्दी (Hindi)',
        'native_name': 'हिन्दी',
        'voice_code': 'hi-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'bengali': {
        'code': LanguageCode.BENGALI.value,
        'name': 'বাংলা (Bengali)',
        'native_name': 'বাংলা',
        'voice_code': 'bn-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'telugu': {
        'code': LanguageCode.TELUGU.value,
        'name': 'తెలుగు (Telugu)',
        'native_name': 'తెలుగు',
        'voice_code': 'te-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'marathi': {
        'code': LanguageCode.MARATHI.value,
        'name': 'मराठी (Marathi)',
        'native_name': 'मराठी',
        'voice_code': 'mr-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'tamil': {
        'code': LanguageCode.TAMIL.value,
        'name': 'தமிழ் (Tamil)',
        'native_name': 'தமிழ்',
        'voice_code': 'ta-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'kannada': {
        'code': LanguageCode.KANNADA.value,
        'name': 'ಕನ್ನಡ (Kannada)',
        'native_name': 'ಕನ್ನಡ',
        'voice_code': 'kn-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'gujarati': {
        'code': LanguageCode.GUJARATI.value,
        'name': 'ગુજરાતી (Gujarati)',
        'native_name': 'ગુજરાતી',
        'voice_code': 'gu-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'malayalam': {
        'code': LanguageCode.MALAYALAM.value,
        'name': 'മലയാളം (Malayalam)',
        'native_name': 'മലയാളം',
        'voice_code': 'ml-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'punjabi': {
        'code': LanguageCode.PUNJABI.value,
        'name': 'ਪੰਜਾਬੀ (Punjabi)',
        'native_name': 'ਪੰਜਾਬੀ',
        'voice_code': 'pa-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
    'urdu': {
        'code': LanguageCode.URDU.value,
        'name': 'اردو (Urdu)',
        'native_name': 'اردو',
        'voice_code': 'ur-IN',
        'flag': '🇮🇳',
        'is_rtl': True,
        'supported': True
    },
    'odia': {
        'code': LanguageCode.ODIA.value,
        'name': 'ଓଡ଼ିଆ (Odia)',
        'native_name': 'ଓଡ଼ିଆ',
        'voice_code': 'or-IN',
        'flag': '🇮🇳',
        'is_rtl': False,
        'supported': True
    },
}


class MultilingualProcessor:
    """
    Main class for handling multilingual operations
    Supports translation, language detection, and formatting
    """

    def __init__(self):
        """Initialize the multilingual processor"""
        self.translator = None
        self.cache_size = 128
        self.translation_cache = {}

    def translate_text(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Tuple[str, bool]:
        """
        Translate text using MyMemory API or dictionary fallback
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: 'auto' for auto-detect)
            target_lang: Target language code (default: 'en')
            
        Returns:
            Tuple of (translated_text, success_flag)
        """
        if not text or text.strip() == '':
            return text, True
            
        # Map language names to codes
        source_code = self._get_lang_code(source_lang)
        target_code = self._get_lang_code(target_lang)

        # Check cache first
        cache_key = f"{source_code}_{target_code}_{text[:50]}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key], True

        # If source and target are same, return original
        if source_code == target_code:
            return text, True

        # Try MyMemory API first (free, no key needed)
        if requests_available:
            try:
                translated = self._translate_mymemory(text, source_code, target_code)
                if translated and translated != text:
                    self.translation_cache[cache_key] = translated
                    logger.info(f"✓ Translated {source_code}→{target_code} via MyMemory API")
                    return translated, True
            except Exception as e:
                logger.debug(f"MyMemory API failed: {e}")

        # Fallback to dictionary-based translation
        try:
            translated = self._translate_dictionary(text, source_code, target_code)
            self.translation_cache[cache_key] = translated
            logger.info(f"✓ Translated {source_code}→{target_code} via dictionary fallback")
            return translated, True
        except Exception as e:
            logger.warning(f"Translation fallback failed: {e}")
            return text, False

    def _translate_mymemory(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate using free MyMemory API"""
        try:
            import requests
            url = "https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': f'{source_lang}|{target_lang}'
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('responseStatus') == 200:
                    translated = data['responseData'].get('translatedText', text)
                    return translated
        except Exception as e:
            logger.debug(f"MyMemory API error: {e}")
        return text

    def _translate_dictionary(self, text: str, source_lang: str, target_lang: str) -> str:
        """Fallback dictionary-based translation"""
        if source_lang == 'en':
            # Translate from English to target language
            pair_key = f'en_{target_lang}'
            if pair_key in BASIC_TRANSLATIONS:
                translations = BASIC_TRANSLATIONS[pair_key]
                words = text.lower().split()
                translated_words = []
                for word in words:
                    # Remove punctuation and check dictionary
                    clean_word = word.strip('.,!?;:')
                    translated_words.append(translations.get(clean_word, word))
                return ' '.join(translated_words)
        
        # For other cases, return original text
        return text

    def detect_language(self, text: str) -> Tuple[str, str, float]:
        """
        Detect the language of the input text using character patterns
        
        Args:
            text: Text to detect language for
            
        Returns:
            Tuple of (language_code, language_name, confidence)
        """
        if not text or text.strip() == '':
            return 'en', 'English', 0.0

        # Character ranges for different scripts
        devanagari_range = range(0x0900, 0x097F)  # Hindi, Marathi, Sanskrit
        bengali_range = range(0x0980, 0x09FF)     # Bengali, Assamese, Odia
        gurmukhi_range = range(0x0A00, 0x0A7F)   # Punjabi
        gujarati_range = range(0x0A80, 0x0AFF)   # Gujarati
        oriya_range = range(0x0B00, 0x0B7F)      # Odia
        tamil_range = range(0x0B80, 0x0BFF)      # Tamil
        telugu_range = range(0x0C60, 0x0C7F)     # Telugu
        kannada_range = range(0x0C80, 0x0CFF)    # Kannada
        malayalam_range = range(0x0D00, 0x0D7F)  # Malayalam
        arabic_range = range(0x0600, 0x06FF)     # Urdu, Arabic

        # Count characters in each script
        char_counts = {
            'devanagari': 0, 'bengali': 0, 'gurmukhi': 0, 'gujarati': 0,
            'oriya': 0, 'tamil': 0, 'telugu': 0, 'kannada': 0, 'malayalam': 0,
            'arabic': 0, 'latin': 0
        }

        for char in text:
            code = ord(char)
            if code in devanagari_range:
                char_counts['devanagari'] += 1
            elif code in bengali_range:
                char_counts['bengali'] += 1
            elif code in gurmukhi_range:
                char_counts['gurmukhi'] += 1
            elif code in gujarati_range:
                char_counts['gujarati'] += 1
            elif code in oriya_range:
                char_counts['oriya'] += 1
            elif code in tamil_range:
                char_counts['tamil'] += 1
            elif code in telugu_range:
                char_counts['telugu'] += 1
            elif code in kannada_range:
                char_counts['kannada'] += 1
            elif code in malayalam_range:
                char_counts['malayalam'] += 1
            elif code in arabic_range:
                char_counts['arabic'] += 1
            elif 32 <= code <= 126:  # ASCII letters
                char_counts['latin'] += 1

        # Map script to language
        script_to_lang = {
            'devanagari': ('hi', 'Hindi'),
            'bengali': ('bn', 'Bengali'),
            'gurmukhi': ('pa', 'Punjabi'),
            'gujarati': ('gu', 'Gujarati'),
            'oriya': ('or', 'Odia'),
            'tamil': ('ta', 'Tamil'),
            'telugu': ('te', 'Telugu'),
            'kannada': ('kn', 'Kannada'),
            'malayalam': ('ml', 'Malayalam'),
            'arabic': ('ur', 'Urdu'),
            'latin': ('en', 'English'),
        }

        # Find the script with most characters
        max_script = max(char_counts, key=char_counts.get)
        max_count = char_counts[max_script]

        if max_count == 0:
            # No characters detected, assume English
            return 'en', 'English', 0.0

        # Calculate confidence
        total_chars = len([c for c in text if ord(c) > 32])
        confidence = max_count / total_chars if total_chars > 0 else 0.0

        lang_code, lang_name = script_to_lang[max_script]
        logger.info(f"✓ Detected language: {lang_name} ({lang_code}) with confidence {confidence:.2f}")
        
        return lang_code, lang_name, confidence

    def get_supported_languages(self) -> Dict[str, Dict]:
        """Get list of supported languages"""
        return INDIAN_LANGUAGES

    def get_language_info(self, lang_key: str) -> Optional[Dict]:
        """
        Get information about a specific language
        
        Args:
            lang_key: Language key (e.g., 'hindi', 'bengali')
            
        Returns:
            Language information dictionary or None if not found
        """
        return INDIAN_LANGUAGES.get(lang_key.lower())

    def format_for_language(
        self,
        text: str,
        lang_code: str
    ) -> str:
        """
        Format text according to language-specific rules
        
        Args:
            text: Text to format
            lang_code: Language code
            
        Returns:
            Formatted text
        """
        lang_info = None
        for key, info in INDIAN_LANGUAGES.items():
            if info['code'] == lang_code:
                lang_info = info
                break

        if not lang_info:
            return text

        # RTL language formatting
        if lang_info.get('is_rtl'):
            return self._format_rtl_text(text)

        return text

    def _format_rtl_text(self, text: str) -> str:
        """Format text for right-to-left languages"""
        # Add RTL markers for proper rendering
        return f"\u202e{text}\u202c"

    def _get_lang_code(self, lang_identifier: str) -> str:
        """
        Convert language identifier to language code
        Handles both language names and codes
        """
        if len(lang_identifier) == 2:
            return lang_identifier.lower()

        # Check if it's a language name
        for key, info in INDIAN_LANGUAGES.items():
            if lang_identifier.lower() == key or \
               lang_identifier.lower() == info['name'].lower() or \
               lang_identifier.lower() == info['native_name'].lower():
                return info['code']

        # Default to English
        return 'en'

    def batch_translate(
        self,
        texts: List[str],
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Tuple[List[str], bool]:
        """
        Translate multiple texts at once
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Tuple of (translated_texts, success_flag)
        """
        try:
            translated_texts = []
            for text in texts:
                translated, _ = self.translate_text(text, source_lang, target_lang)
                translated_texts.append(translated)
            return translated_texts, True
        except Exception as e:
            logger.error(f"Batch translation error: {e}")
            return texts, False

    def get_language_selector_options(self) -> List[Tuple[str, str]]:
        """
        Get formatted options for language selector UI
        
        Returns:
            List of (display_name, language_key) tuples
        """
        options = []
        for key, info in INDIAN_LANGUAGES.items():
            if info.get('supported'):
                display_name = f"{info['flag']} {info['name']}"
                options.append((display_name, key))
        return sorted(options, key=lambda x: x[1])

    def get_voice_code_for_language(self, lang_key: str) -> str:
        """Get the voice code for a language"""
        lang_info = self.get_language_info(lang_key)
        if lang_info:
            return lang_info.get('voice_code', 'en-IN')
        return 'en-IN'

    def validate_language_code(self, lang_code: str) -> bool:
        """Check if a language code is supported"""
        for info in INDIAN_LANGUAGES.values():
            if info['code'] == lang_code:
                return True
        return False


# Singleton instance
_processor_instance = None


def get_multilingual_processor() -> MultilingualProcessor:
    """Get or create the multilingual processor singleton"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = MultilingualProcessor()
    return _processor_instance


# Convenient module-level functions
def translate(
    text: str,
    source_lang: str = 'auto',
    target_lang: str = 'en'
) -> str:
    """Translate text (convenience function)"""
    processor = get_multilingual_processor()
    translated, _ = processor.translate_text(text, source_lang, target_lang)
    return translated


def detect_language(text: str) -> str:
    """Detect language of text (convenience function)"""
    processor = get_multilingual_processor()
    lang_code, _, _ = processor.detect_language(text)
    return lang_code


def get_supported_languages() -> Dict[str, Dict]:
    """Get all supported languages (convenience function)"""
    processor = get_multilingual_processor()
    return processor.get_supported_languages()
