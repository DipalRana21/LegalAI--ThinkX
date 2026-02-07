# Multilingual Support Module - Documentation

## Overview

The LegalAI application now includes comprehensive multilingual support for Indian languages, enabling users to interact with the legal assistance system in their preferred language. This module provides seamless translation, language detection, and localized user interface components.

## Features

### 1. **Multi-Language Support**
Supports 12 major Indian languages plus English:
- 🇬🇧 **English** (en)
- 🇮🇳 **Hindi** (हिन्दी) (hi)
- 🇮🇳 **Bengali** (বাংলা) (bn)
- 🇮🇳 **Telugu** (తెలుగు) (te)
- 🇮🇳 **Marathi** (मराठी) (mr)
- 🇮🇳 **Tamil** (தமிழ்) (ta)
- 🇮🇳 **Kannada** (ಕನ್ನಡ) (kn)
- 🇮🇳 **Gujarati** (ગુજરાતી) (gu)
- 🇮🇳 **Malayalam** (മലയാളം) (ml)
- 🇮🇳 **Punjabi** (ਪੰਜਾਬੀ) (pa)
- 🇮🇳 **Urdu** (اردو) (ur) *[RTL Support]*
- 🇮🇳 **Odia** (ଓଡ଼ିଆ) (or)

### 2. **Core Modules**

#### **backend/multilingual.py**
Main module for multilingual operations:
- `MultilingualProcessor` class for translations and language detection
- Automatic language detection
- Batch translation support
- Language validation and formatting
- Voice code mapping for each language

**Key Functions:**
```python
# Get processor instance
processor = get_multilingual_processor()

# Translate text
translated, success = processor.translate_text(text, 'en', 'hi')

# Detect language
lang_code, lang_name, confidence = processor.detect_language(text)

# Get language info
info = processor.get_language_info('hindi')
voice_code = processor.get_voice_code_for_language('hindi')
```

#### **backend/language_strings.py**
Comprehensive localization source:
- UI strings in all supported languages
- Legal terminology translations
- Help messages and guidance text
- `get_string()` function for localized strings

**Key Functions:**
```python
# Get localized string
label = get_string('app_title', 'hi', 'general')

# Get all strings for a language
all_strings = get_all_strings('en')

# Get supported language list
languages = get_supported_languages_list()
```

#### **backend/language_prompts.py**
Language-specific prompts and context:
- System prompts tailored for each language
- Query enhancement templates
- Legal context mapping
- Response formatting templates
- Legal term translation utilities

**Key Functions:**
```python
# Get system prompt
prompt = get_system_prompt('hi')

# Enhance query with context
enhanced = enhance_query_for_language(query, 'hi', 'general')
```

#### **frontend/multilingual_ui.py**
Interactive UI components:
- `MultilingualUI` class for UI rendering
- Language selector components
- Voice input/output language settings
- Response language preferences
- Translation options
- Language statistics and information panels

**Key Functions:**
```python
# Render complete multilingual sidebar
settings = render_multilingual_sidebar()

# Get current language settings
current = get_current_language_settings()
```

### 3. **User Interface Integration**

The multilingual UI integrates seamlessly into the sidebar with:

1. **Language Selector** - Choose preferred interface language
2. **Voice Input Settings** - Select language for voice input
3. **Response Language** - Choose language for AI responses
4. **Translation Options** - Enable/disable auto-translation
5. **Language Info Panel** - View details about selected language
6. **Language Statistics** - See supported languages and capabilities

### 4. **Voice Support**

Integration with voice input/output:
- Language-specific voice codes (e.g., 'hi-IN', 'ta-IN')
- Voice extraction from selected language
- Automatic voice routing based on language selection

### 5. **Translation Engine**

Uses Google Translate API with:
- Automatic language detection
- Context-aware translation
- Batch translation support
- Fallback mechanisms for API failures
- Error logging and user feedback

## Installation

### 1. **Update Dependencies**

The following have been added to `requirements.txt`:
```
googletrans==4.0.0rc1
librosa>=0.11.0
```

Install using:
```bash
pip install -r requirements.txt
```

### 2. **Verify Installation**

```bash
python -c "from backend.multilingual import get_multilingual_processor; print(get_multilingual_processor())"
```

## Usage

### Basic Usage in Streamlit App

```python
# In frontend/app.py (already integrated)
from frontend.multilingual_ui import render_multilingual_sidebar

# In sidebar
language_settings = render_multilingual_sidebar()

# Access current settings
current_lang = st.session_state.user_language
voice_lang = st.session_state.voice_language
response_lang = st.session_state.response_language
```

### Translate Text

```python
from backend.multilingual import translate

# Simple translation
hindi_text = translate("What is the punishment for theft?", 'en', 'hi')
```

### Get Localized Strings

```python
from backend.language_strings import get_string

# Get localized UI string
title = get_string('app_title', 'hi', 'general')
legal_term = get_string('section', 'ta', 'legal')
help_text = get_string('voice_input_help', 'bn', 'help')
```

### Use Language-Specific Prompts

```python
from backend.language_prompts import get_prompt_manager

manager = get_prompt_manager()

# Get system prompt for language
prompt = manager.get_system_prompt('hi')

# Enhance query for better results
enhanced_query = manager.enhance_query(
    "What are the rights of the accused?",
    language_code='hi',
    query_type='general'
)

# Get legal context
context = manager.get_legal_context("मुझ पर चोरी का आरोप है", 'hi')
# Output: {'crime_related': ['चोरी']}
```

## Configuration

### Language Metadata

Each language in `INDIAN_LANGUAGES` includes:
- `code`: ISO 639-1 language code
- `name`: English name of language
- `native_name`: Name in the language itself
- `voice_code`: Language code for voice synthesis (e.g., 'hi-IN')
- `flag`: Country flag emoji
- `is_rtl`: Boolean for right-to-left text support
- `supported`: Boolean indicating if language is supported

### Adding New Languages

To add a new language:

1. **Update `backend/multilingual.py`:**
```python
INDIAN_LANGUAGES = {
    'spanish': {
        'code': 'es',
        'name': 'Español (Spanish)',
        'native_name': 'Español',
        'voice_code': 'es-ES',
        'flag': '🇪🇸',
        'is_rtl': False,
        'supported': True
    },
    # ... existing languages
}
```

2. **Add UI Strings in `backend/language_strings.py`:**
```python
LANGUAGE_STRINGS['es'] = {
    'app_title': 'NyayaSahayak - Asistencia Jurídica India',
    'language_selector': 'Seleccionar idioma',
    # ... more strings
}
```

3. **Add System Prompt in `backend/language_prompts.py`:**
```python
SYSTEM_PROMPTS['es'] = """Your system prompt in Spanish..."""
```

## API Reference

### MultilingualProcessor

```python
class MultilingualProcessor:
    def translate_text(text, source_lang='auto', target_lang='en') 
        -> Tuple[str, bool]
    
    def detect_language(text) -> Tuple[str, str, float]
    
    def get_supported_languages() -> Dict[str, Dict]
    
    def get_language_info(lang_key) -> Optional[Dict]
    
    def format_for_language(text, lang_code) -> str
    
    def batch_translate(texts, source_lang='auto', target_lang='en') 
        -> Tuple[List[str], bool]
    
    def get_language_selector_options() -> List[Tuple[str, str]]
    
    def get_voice_code_for_language(lang_key) -> str
    
    def validate_language_code(lang_code) -> bool
```

### MultilingualUI

```python
class MultilingualUI:
    def render_css() -> None
    
    def render_language_selector() -> str
    
    def render_voice_input_selector() -> str
    
    def render_response_language_selector() -> str
    
    def render_language_tabs(languages=None) -> str
    
    def render_translation_options() -> Dict[str, bool]
    
    def translate_response(text, target_lang) -> Tuple[str, bool]
    
    def render_language_stats() -> None
    
    def render_language_info_panel() -> None
    
    def get_localized_string(key, category='general') -> str
```

### LanguageSpecificPromptManager

```python
class LanguageSpecificPromptManager:
    def get_system_prompt(language_code) -> str
    
    def enhance_query(query, language_code='en', 
                     query_type='general') -> str
    
    def get_legal_context(query, language_code='en') 
        -> Dict[str, List[str]]
    
    def format_response(response_type, language_code='en', 
                       **kwargs) -> str
    
    def translate_legal_term(term, from_language='en', 
                            to_language='en') -> Optional[str]
    
    def get_language_specific_tips(language_code) -> List[str]
```

## Session State Variables

The application manages the following session state variables:

```python
st.session_state.user_language          # Main UI language (default: 'english')
st.session_state.voice_language         # Voice input language (default: 'english')
st.session_state.response_language      # Response language (default: 'english')
st.session_state.translation_enabled    # Auto-translation toggle (default: False)
st.session_state.rtl_mode              # RTL text mode for Urdu, etc. (default: False)
```

## Error Handling

The module includes robust error handling:

```python
# Translation failures fall back to original text
translated, success = processor.translate_text(text, 'en', 'hi')
if not success:
    # Use original text and log error
    text_to_use = text
```

## Performance Considerations

1. **Caching** - Language processor uses singleton pattern to avoid repeated initialization
2. **Batch Operations** - Use `batch_translate()` for multiple texts
3. **API Limits** - Google Translate has rate limits; consider caching translations
4. **Voice Codes** - Pre-computed for quick access

## Testing

### Test Basic Functionality

```python
# Test translation
from backend.multilingual import translate
result = translate("Hello", "en", "hi")
print(result)  # Should print Hindi translation

# Test language detection
from backend.multilingual import detect_language
lang = detect_language("नमस्ते")
print(lang)  # Should print 'hi'
```

## File Structure

```
backend/
├── multilingual.py           # Main multilingual processor
├── language_strings.py       # Localized UI strings
└── language_prompts.py       # Language-specific prompts

frontend/
└── multilingual_ui.py        # Streamlit UI components

requirements.txt              # Updated with multilingual dependencies
```

## Known Limitations

1. **Google Translate Dependencies** - Requires internet connection
2. **API Rate Limits** - Google Translate has usage limits
3. **Context Accuracy** - Translation quality depends on context
4. **RTL Support** - Limited RTL support; may need CSS adjustments

## Future Enhancements

1. Local translation models (Hugging Face)
2. Caching layer for frequent translations
3. Custom legal terminology database
4. Audio/speech-to-speech capabilities
5. Offline translation support
6. Machine learning-based context understanding
7. Speech synthesis for responses (multi-language TTS)
8. Regional dialect support

## Support and Troubleshooting

### Issue: Translation not working

**Solution**: Check internet connection and Google Translate service status

### Issue: Voice input not working

**Solution**: Ensure `streamlit-mic-recorder` is installed and browser has microphone permissions

### Issue: RTL text rendering issues

**Solution**: Clear browser cache and check CSS in `multilingual_ui.py`

### Issue: Language option not appearing

**Solution**: Verify `MULTILINGUAL_AVAILABLE` is `True` in `app.py`

## Contributing

To contribute improvements:

1. Add new languages to `INDIAN_LANGUAGES`
2. Provide translations for all UI strings
3. Add language-specific prompts
4. Test with actual user queries
5. Submit feedback or improvements

## License

This multilingual module is part of the LegalAI project and follows the same license.

## Author Notes

The multilingual support system is designed with the following principles:

- **Inclusivity**: Support for all major Indian languages
- **Flexibility**: Easy to add new languages
- **Robustness**: Graceful fallbacks and error handling
- **Performance**: Efficient caching and singleton patterns
- **User Experience**: Interactive and intuitive UI
- **Accuracy**: Legal terminology preservation across languages

For questions or issues, please refer to the main project documentation or contact the development team.
