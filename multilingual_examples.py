"""
Multilingual Module - Usage Examples and Demonstrations
Shows practical examples of using the multilingual support system
"""

from backend.multilingual import (
    get_multilingual_processor,
    translate,
    detect_language,
    get_supported_languages,
    INDIAN_LANGUAGES
)
from backend.language_strings import (
    get_string,
    get_all_strings,
    LANGUAGE_STRINGS,
    LEGAL_TERMS,
    get_supported_languages_list
)
from backend.language_prompts import (
    get_prompt_manager,
    get_system_prompt,
    enhance_query_for_language
)


def example_basic_translation():
    """Example 1: Basic Text Translation"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Text Translation")
    print("=" * 60)
    
    processor = get_multilingual_processor()
    
    # English to Hindi
    text_en = "What is the punishment for theft?"
    text_hi, success = processor.translate_text(text_en, 'en', 'hi')
    print(f"English: {text_en}")
    print(f"Hindi: {text_hi}")
    print(f"Success: {success}\n")
    
    # English to Tamil
    text_ta, success = processor.translate_text(text_en, 'en', 'ta')
    print(f"Tamil: {text_ta}")
    print(f"Success: {success}\n")


def example_language_detection():
    """Example 2: Language Detection"""
    print("=" * 60)
    print("EXAMPLE 2: Language Detection")
    print("=" * 60)
    
    processor = get_multilingual_processor()
    
    # Test texts in different languages
    test_texts = {
        'English': "What are my rights under the Constitution?",
        'Hindi': "मुझे चोरी का आरोप है, मेरे क्या अधिकार हैं?",
        'Bengali': "সম্পত্তি বিরোধে আমি কি করতে পারি?",
        'Tamil': "திருட்டுக்கான தண்டனை என்ன?",
    }
    
    for lang_name, text in test_texts.items():
        lang_code, lang_name_detected, confidence = processor.detect_language(text)
        print(f"{lang_name}: {text}")
        print(f"  → Detected: {lang_name_detected} ({lang_code}), Confidence: {confidence}")
        print()


def example_get_language_info():
    """Example 3: Get Language Information"""
    print("=" * 60)
    print("EXAMPLE 3: Language Information")
    print("=" * 60)
    
    processor = get_multilingual_processor()
    
    # Get info for specific languages
    for lang_key in ['hindi', 'bengali', 'tamil', 'urdu']:
        info = processor.get_language_info(lang_key)
        print(f"{info['flag']} {info['name']}")
        print(f"  Code: {info['code']}")
        print(f"  Voice Code: {info['voice_code']}")
        print(f"  Native: {info['native_name']}")
        print(f"  RTL: {info.get('is_rtl', False)}")
        print()


def example_ui_localization():
    """Example 4: UI String Localization"""
    print("=" * 60)
    print("EXAMPLE 4: UI Localization")
    print("=" * 60)
    
    # Get strings for different languages
    key = 'app_title'
    
    for lang_code in ['en', 'hi', 'bn', 'ta']:
        localized = get_string(key, lang_code, 'general')
        print(f"{lang_code}: {localized}")
    
    print("\n" + "=" * 60)
    print("Legal Terms Translation")
    print("=" * 60)
    
    term = 'section'
    print(f"English: {get_string(term, 'en', 'legal')}")
    print(f"Hindi: {get_string(term, 'hi', 'legal')}")
    print(f"Bengali: {get_string(term, 'bn', 'legal')}")
    print(f"Tamil: {get_string(term, 'ta', 'legal')}")
    print()


def example_batch_translation():
    """Example 5: Batch Translation"""
    print("=" * 60)
    print("EXAMPLE 5: Batch Translation")
    print("=" * 60)
    
    processor = get_multilingual_processor()
    
    queries = [
        "What is the Indian Penal Code?",
        "Explain Article 21 of Constitution",
        "What are bail provisions?"
    ]
    
    print("Original (English):")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")
    
    # Translate to Hindi
    translated, success = processor.batch_translate(queries, 'en', 'hi')
    
    print(f"\nTranslated to Hindi (Success: {success}):")
    for i, q in enumerate(translated, 1):
        print(f"  {i}. {q}")
    print()


def example_language_selection_ui():
    """Example 6: Language Selection UI Options"""
    print("=" * 60)
    print("EXAMPLE 6: Language Selection Options")
    print("=" * 60)
    
    processor = get_multilingual_processor()
    
    options = processor.get_language_selector_options()
    
    print("Available Languages for UI Selector:")
    for display_name, lang_key in options:
        print(f"  {display_name} → {lang_key}")
    
    print(f"\nTotal: {len(options)} languages")
    print()


def example_voice_codes():
    """Example 7: Voice Codes for Each Language"""
    print("=" * 60)
    print("EXAMPLE 7: Voice Codes for Speech Synthesis")
    print("=" * 60)
    
    processor = get_multilingual_processor()
    
    languages = ['english', 'hindi', 'bengali', 'tamil', 'telugu']
    
    print("Language → Voice Code")
    for lang_key in languages:
        voice_code = processor.get_voice_code_for_language(lang_key)
        lang_info = INDIAN_LANGUAGES[lang_key]
        print(f"  {lang_info['name']:20} → {voice_code}")
    print()


def example_language_specific_prompts():
    """Example 8: Language-Specific Prompts"""
    print("=" * 60)
    print("EXAMPLE 8: Language-Specific Prompts")
    print("=" * 60)
    
    manager = get_prompt_manager()
    
    # Get system prompt for English
    print("English System Prompt (first 200 chars):")
    prompt_en = manager.get_system_prompt('en')
    print(f"  {prompt_en[:200]}...\n")
    
    # Get system prompt for Hindi
    print("Hindi System Prompt (first 200 chars):")
    prompt_hi = manager.get_system_prompt('hi')
    print(f"  {prompt_hi[:200]}...\n")


def example_query_enhancement():
    """Example 9: Query Enhancement for Different Languages"""
    print("=" * 60)
    print("EXAMPLE 9: Query Enhancement")
    print("=" * 60)
    
    manager = get_prompt_manager()
    
    query = "What are the rights of an accused?"
    
    print("Original Query:")
    print(f"  English: {query}\n")
    
    # Enhance for different language contexts
    for lang_code in ['en', 'hi']:
        enhanced = manager.enhance_query(query, lang_code, 'general')
        print(f"Enhanced for {lang_code}:")
        print(f"  {enhanced}\n")


def example_legal_context():
    """Example 10: Legal Context Identification"""
    print("=" * 60)
    print("EXAMPLE 10: Legal Context Identification")
    print("=" * 60)
    
    manager = get_prompt_manager()
    
    # Test queries
    queries = {
        'English': "I have been accused of theft. What are my rights?",
        'Hindi': "मुझ पर चोरी का आरोप है। मेरे क्या अधिकार हैं?",
    }
    
    for lang, query in queries.items():
        lang_code = 'en' if lang == 'English' else 'hi'
        context = manager.get_legal_context(query, lang_code)
        
        print(f"{lang}:")
        print(f"  Query: {query}")
        print(f"  Identified Context: {context}")
        print()


def example_legal_terminology():
    """Example 11: Legal Terminology Across Languages"""
    print("=" * 60)
    print("EXAMPLE 11: Legal Terminology Translation")
    print("=" * 60)
    
    # Common legal terms
    legal_terms = ['section', 'bail', 'petition', 'jurisdiction', 'offense']
    
    print("Legal Terms in Different Languages:\n")
    
    for term in legal_terms:
        print(f"{term.upper()}:")
        print(f"  English: {get_string(term, 'en', 'legal')}")
        print(f"  Hindi: {get_string(term, 'hi', 'legal')}")
        print(f"  Bengali: {get_string(term, 'bn', 'legal')}")
        print()


def example_full_localization():
    """Example 12: Complete UI Localization"""
    print("=" * 60)
    print("EXAMPLE 12: Full UI Localization")
    print("=" * 60)
    
    for lang_code in ['en', 'hi', 'bn']:
        print(f"\n{lang_code.upper()} Localization:")
        print("-" * 40)
        
        lang_name = INDIAN_LANGUAGES.get(
            [k for k, v in INDIAN_LANGUAGES.items() if v['code'] == lang_code][0],
            {}
        ).get('name', 'Unknown')
        
        print(f"Language: {lang_name}")
        print(f"  Title: {get_string('app_title', lang_code, 'general')}")
        print(f"  Subtitle: {get_string('app_subtitle', lang_code, 'general')}")
        print(f"  Submit Label: {get_string('submit_query', lang_code, 'general')}")
        print(f"  Help Text: {get_string('help', lang_code, 'general')}")


def example_translation_with_fallback():
    """Example 13: Translation with Fallback"""
    print("=" * 60)
    print("EXAMPLE 13: Translation with Graceful Fallback")
    print("=" * 60)
    
    processor = get_multilingual_processor()
    
    text = "This is an important legal concept"
    
    # Try translation with fallback
    translated, success = processor.translate_text(text, 'en', 'hi')
    
    print(f"Original: {text}")
    print(f"Translated: {translated}")
    print(f"Success: {success}")
    
    if not success:
        print("Note: Translation failed, original text returned")
    print()


def run_all_examples():
    """Run all examples"""
    print("\n" * 2)
    print("█" * 60)
    print("MULTILINGUAL MODULE - USAGE EXAMPLES".center(60))
    print("█" * 60)
    print()
    
    examples = [
        (example_basic_translation, "Basic Translation"),
        (example_language_detection, "Language Detection"),
        (example_get_language_info, "Language Information"),
        (example_ui_localization, "UI Localization"),
        (example_batch_translation, "Batch Translation"),
        (example_language_selection_ui, "Language Selection UI"),
        (example_voice_codes, "Voice Codes"),
        (example_language_specific_prompts, "Language-Specific Prompts"),
        (example_query_enhancement, "Query Enhancement"),
        (example_legal_context, "Legal Context"),
        (example_legal_terminology, "Legal Terminology"),
        (example_full_localization, "Full Localization"),
        (example_translation_with_fallback, "Translation with Fallback"),
    ]
    
    for i, (example_func, title) in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"⚠️ Error in {title}: {e}\n")
    
    print("\n" * 1)
    print("█" * 60)
    print("All examples completed!".center(60))
    print("█" * 60)


if __name__ == "__main__":
    # Run all examples
    run_all_examples()
    
    # Or run a specific example:
    # example_basic_translation()
    # example_language_detection()
    # etc.
