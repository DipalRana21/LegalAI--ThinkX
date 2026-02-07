#!/usr/bin/env python
"""Quick test to verify all languages are loaded"""

from backend.multilingual import INDIAN_LANGUAGES

print(f'✓ Total Languages Supported: {len(INDIAN_LANGUAGES)}\n')
print('='*60)
print('All Supported Languages:\n')

for i, (key, info) in enumerate(INDIAN_LANGUAGES.items(), 1):
    flag = info["flag"]
    name = info["name"]
    code = info["code"]
    voice = info["voice_code"]
    rtl = "RTL" if info.get("is_rtl") else "LTR"
    
    print(f'{i:2}. {flag} {name:30} | {code:2} | {voice:7} | {rtl}')

print('\n' + '='*60)
print(f'✓ All {len(INDIAN_LANGUAGES)} languages are properly configured!')
