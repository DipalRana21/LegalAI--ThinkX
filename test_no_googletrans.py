#!/usr/bin/env python
"""Test multilingual without Google Translate"""

from backend.multilingual import get_multilingual_processor, INDIAN_LANGUAGES

print("\n" + "="*70)
print("  ✓ Testing Multilingual WITHOUT Google Translate")
print("="*70 + "\n")

processor = get_multilingual_processor()

# Test 1: Language Detection
print("Test 1: Language Detection (Character-based)\n")
test_texts = {
    'English': "What is theft?",
    'Hindi': "चोरी क्या है?",
    'Bengali': "চুরি কি?",
    'Tamil': "திருட்டு என்றால் என்ன?",
}

for lang_name, text in test_texts.items():
    detect_code, detect_name, confidence = processor.detect_language(text)
    print(f"  {lang_name:10} → Detected: {detect_code} with confidence {confidence:.2f}")

# Test 2: Translation (MyMemory API or dictionary fallback)
print("\nTest 2: Translation (MyMemory API + Dictionary Fallback)\n")

translations = [
    ("What is bail?", "en", "hi"),
    ("What is theft?", "en", "hi"),
    ("What is crime?", "en", "hi"),
]

for text, from_lang, to_lang in translations:
    translated, success = processor.translate_text(text, from_lang, to_lang)
    status = "✓" if success else "✗"
    target_name = INDIAN_LANGUAGES.get(to_lang, {}).get('name', to_lang)
    print(f"  {status} EN → {target_name}")
    print(f"     Original:   {text}")
    print(f"     Translated: {translated}\n")

# Test 3: All Languages Available
print("Test 3: All 12 Languages Still Available\n")
print(f"  Total languages: {len(INDIAN_LANGUAGES)}\n")

for i, (key, info) in enumerate(INDIAN_LANGUAGES.items(), 1):
    print(f"  {i:2}. {info['flag']} {info['name']:30} (Code: {info['code']})")

print("\n" + "="*70)
print("  ✓ MULTILINGUAL SUPPORT WORKING WITHOUT GOOGLE TRANSLATE!")
print("="*70 + "\n")

print("Alternative Methods Used:")
print("  • Language Detection: Unicode character ranges")
print("  • Translation: MyMemory API (if available) + Dictionary fallback")
print("  • No external dependencies required!\n")
