# Multilingual Support - Quick Start Guide

## What's New?

LegalAI now supports **12 Indian languages** with interactive multilingual interface, translation capabilities, and language-aware responses.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The following new packages are added:
- `googletrans==4.0.0rc1` - Translation API
- `librosa>=0.11.0` - Audio processing

### 2. Run the Application

```bash
streamlit run frontend/app.py
```

### 3. Use Language Features

Once the app loads, look for the **🌍 Language & Accessibility** section in the sidebar:

#### **Select Your Language**
- Choose your preferred interface language
- The UI elements update immediately
- Available languages shown with flags and native names

#### **Voice Input Settings**
- Select language for voice input
- Click microphone and speak
- System transcribes in selected language

#### **Response Language**
- Choose language for AI responses
- Responses are translated if needed
- Native speakers get better context

#### **Translation Options**
- Enable/disable auto-translation
- Show original text alongside translation
- Flexible translation settings

## Supported Languages

| Language | Code | Flag | Native Name |
|----------|------|------|------------|
| English | en | 🇬🇧 | English |
| Hindi | hi | 🇮🇳 | हिन्दी |
| Bengali | bn | 🇮🇳 | বাংলা |
| Telugu | te | 🇮🇳 | తెలుగు |
| Marathi | mr | 🇮🇳 | मराठी |
| Tamil | ta | 🇮🇳 | தமிழ் |
| Kannada | kn | 🇮🇳 | ಕನ್ನಡ |
| Gujarati | gu | 🇮🇳 | ગુજરાતી |
| Malayalam | ml | 🇮🇳 | മലയാളം |
| Punjabi | pa | 🇮🇳 | ਪੰਜਾਬੀ |
| Urdu | ur | 🇮🇳 | اردو |
| Odia | or | 🇮🇳 | ଓଡ଼ିଆ |

## Features Explained

### 🎤 Voice Input in Any Language
- Speak naturally in your language
- System transcribes accurately
- Works with voice-enabled devices

### 💬 Responses in Your Language
- AI responses translated to selected language
- Legal concepts preserved
- Context-aware translation

### 🔄 Auto-Translation
- Enable/disable translation features
- View original and translated text
- Toggle translation on the fly

### 📚 Language Information
- Click "Language Information" to learn about selected language
- See language code, voice code, and properties
- RTL support indicator for Urdu

### 📊 System Overview
- Total languages supported
- Current voice and response languages
- Quick language statistics

## Example Usage

### Asking Questions

**English:**
> "What is the punishment for theft under Indian Penal Code?"

**Hindi:**
> "भारतीय दंड संहिता के तहत चोरी की सजा क्या है?"

**Bengali:**
> "ভারতীয় দণ্ড সংহিতার অধীনে চুরির শাস্তি কী?"

### Using Voice Input

1. Select language from "Voice Input Language" dropdown
2. Click "🎤 Click to Speak" button
3. Speak your question clearly
4. System transcribes and searches legal documents

### Viewing Translated Responses

1. Set "Response Language" to your preferred language
2. Ask a question
3. Response appears in your selected language
4. Toggle "Show Original Text" to see English version

## Interactive UI Components

### Language Selector
```
🌐 Language Settings
- Dropdown to select main language
- Updates entire interface
- Persistent across session
```

### Voice Input Settings
```
🎤 Voice Input Settings
- Select voice input language
- Shows voice code (e.g., hi-IN)
- Guidance for voice input
```

### Response Language
```
💬 Response Language Settings
- Choose output language
- Shows selected language with flag
- RTL mode indicator
```

### Translation Options
```
⚙️ Translation Options
- Enable/disable auto-translation
- Show original text toggle
- Flexible translation settings
```

### Language Statistics
```
📊 System Overview
- Total supported languages
- Current voice language
- Current response language code
```

### Language Information Panel
```
ℹ️ Language Information (Expandable)
- Language name and native name
- Language code and voice code
- RTL support information
- Language status
```

## Configuration

### Change Default Language

Edit `frontend/multilingual_ui.py`:
```python
if 'user_language' not in st.session_state:
    st.session_state.user_language = 'hindi'  # Change this
```

### Add New Language

1. Update `backend/multilingual.py` - Add to `INDIAN_LANGUAGES`
2. Update `backend/language_strings.py` - Add UI strings
3. Update `backend/language_prompts.py` - Add system prompts

## Troubleshooting

### Issue: Language selector not appearing
**Solution:** Ensure `MULTILINGUAL_AVAILABLE = True` in `frontend/app.py`

### Issue: Translation not working
**Solution:** Check internet connection and verify `googletrans` is installed

### Issue: Voice input in different language
**Solution:** Make sure you've selected the correct voice language before clicking microphone

### Issue: RTL text not displaying correctly
**Solution:** Clear brower cache and ensure CSS is loaded properly

## File References

| File | Purpose |
|------|---------|
| `backend/multilingual.py` | Core translation and language processing |
| `backend/language_strings.py` | UI localization strings |
| `backend/language_prompts.py` | Language-specific prompts and context |
| `frontend/multilingual_ui.py` | Interactive UI components |
| `frontend/app.py` | Main app (integrated with multilingual support) |
| `requirements.txt` | Updated dependencies |
| `MULTILINGUAL_DOCUMENTATION.md` | Full technical documentation |

## Best Practices

### When Using Voice Input
- Speak clearly and distinctly
- Use natural speech patterns
- Include relevant keywords (e.g., section numbers)
- One question at a time

### When Translating
- Enable translation for consistency
- Use consistent language throughout session
- Review translations for accuracy
- Report translation issues

### For Best Results
- Provide context in your questions
- Mention relevant sections/articles
- Use specific legal terminology
- Ask follow-up questions for clarity

## Performance Tips

1. **Limit translations** - Too many simultaneous translations may be slow
2. **Cache responses** - Recent translations load faster
3. **Use voice wisely** - Voice processing takes more bandwidth
4. **Clear chat history** - Reduces sidebar clutter

## Legal Disclaimer

⚠️ **Important Notice:**
- This tool is for educational purposes only
- Not a substitute for professional legal advice
- Always consult qualified lawyers for legal matters
- Translations may not capture all legal nuances
- Use at your own discretion

## Support

For issues or suggestions:
1. Check `MULTILINGUAL_DOCUMENTATION.md` for technical details
2. Review error messages in Streamlit logs
3. Verify all dependencies are installed
4. Contact development team for assistance

## What's Different?

### Before (Single Language)
- English only
- Limited voice input support
- No translation features

### After (Multilingual)
- 12 supported languages
- Voice input in all languages
- Automatic translation
- Language-aware responses
- Interactive UI components

## Next Steps

1. ✅ Install dependencies
2. ✅ Run application
3. ✅ Select your language
4. ✅ Try voice input
5. ✅ Ask questions in your language
6. ✅ Explore translation features

Enjoy using LegalAI in your preferred language! 🎉

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Supported Languages:** 12 Indian Languages + English
