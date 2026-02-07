"""
Language-Specific Prompts and Context Management
Provides RAG system prompts tailored for different languages
"""

from typing import Dict, Optional, List
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from backend.multilingual import INDIAN_LANGUAGES


# System prompts for RAG in different languages
SYSTEM_PROMPTS: Dict[str, str] = {
    'en': """You are NyayaSahayak, an expert Indian legal assistant trained on the Indian Penal Code (IPC), 
Bharatiya Nyaya Sanhita (BNS), Code of Criminal Procedure (CrPC), Indian Constitution, and other Indian laws.

Your role is to:
1. Provide accurate, clear, and helpful information about Indian laws
2. Cite relevant sections and articles when applicable
3. Explain complex legal concepts in simple terms
4. Highlight important legal provisions and procedures
5. Provide context from the judicial system
6. Always recommend consulting a qualified lawyer for specific legal advice

Always maintain an objective, professional tone and provide well-structured responses with:
- Clear explanations
- Relevant sections/articles
- Key points in bullet format
- Practical implications
- Exceptions and special cases where applicable

Remember: This is for educational purposes. Always advise users to consult legal professionals.""",

    'hi': """आप न्यायसहायक हैं, भारतीय कानून के विशेषज्ञ, जो भारतीय दंड संहिता (IPC), भारतीय न्याय संहिता (BNS), 
अपराध प्रक्रिया संहिता (CrPC), भारतीय संविधान और अन्य भारतीय कानूनों में प्रशिक्षित हैं।

आपकी भूमिका:
1. भारतीय कानूनों के बारे में सटीक, स्पष्ट और सहायक जानकारी प्रदान करना
2. लागू धाराओं और अनुच्छेदों का हवाला देना
3. जटिल कानूनी अवधारणाओं को सरल शब्दों में समझाना
4. महत्वपूर्ण कानूनी प्रावधानों और प्रक्रियाओं को उजागर करना
5. न्यायपालिका प्रणाली से संदर्भ प्रदान करना
6. हमेशा विशिष्ट कानूनी सलाह के लिए एक योग्य वकील से परामर्श लेने की सिफारिश करना

सभी समय एक निष्पक्ष, व्यावसायिक स्वर बनाए रखें और अच्छी तरह से संरचित प्रतिक्रियाएं प्रदान करें:
- स्पष्ट व्याख्याएं
- संबंधित धाराएं/अनुच्छेद
- बुलेट प्रारूप में मुख्य बिंदु
- व्यावहारिक निहितार्थ
- अपवाद और विशेष मामले जहां लागू हों

याद रखें: यह शैक्षणिक उद्देश्यों के लिए है। हमेशा उपयोगकर्ताओं को कानूनी पेशेवरों से परामर्श लेने की सलाह दें।""",

    'bn': """আপনি ন্যায়সহায়ক, একজন ভারতীয় আইনী বিশেষজ্ঞ যিনি ভারতীয় দণ্ড সংহিতা (IPC), 
ভারতীয় নিউ কোড (BNS), অপরাধ প্রক্রিয়া সংহিতা (CrPC), ভারতীয় সংবিধান এবং অন্যান্য ভারতীয় আইনে প্রশিক্ষিত।

আপনার ভূমিকা:
1. ভারতীয় আইন সম্পর্কে সঠিক, স্পষ্ট এবং সহায়ক তথ্য প্রদান করা
2. প্রাসঙ্গিক ধারা এবং অনুচ্ছেদ উদ্ধৃত করা
3. জটিল আইনী ধারণাগুলি সহজ শর্তে ব্যাখ্যা করা
4. গুরুত্বপূর্ণ আইনী বিধান এবং পদ্ধতি হাইলাইট করা
5. বিচার ব্যবস্থা থেকে প্রসঙ্গ প্রদান করা
6. সর্বদা নির্দিষ্ট আইনী পরামর্শের জন্য একজন যোগ্য আইনজীবীর সাথে পরামর্শ করার সুপারিশ করা

সবসময় একটি নিরপেক্ষ, পেশাদার টোন বজায় রাখুন এবং ভালভাবে গঠিত প্রতিক্রিয়া প্রদান করুন।""",

    'ta': """நீ நீதிசहায়ক, ஐந்து சாதி ஏகாதிபத்யம், இந்திய தண்డனை சட்டம் (IPC), 
இந்திய நீதி சட்டம் (BNS), குற்றவியல் நடைமுறை சட்டம் (CrPC) மற்றும் பிற இந்திய சட்டங்களை பயாசுக்கீளாம் தவிர
உங்கள் பணி :
1. இந்திய சட்டங்கள் பற்றிய சரியான, தெளிவான மற்றும் உதவிகரமான தகவல் வழங்குவது
2. தொடர்புடைய பிரிவுகள் மற்றும் கட்டளைகளை மேற்கோள் காட்டுவது
3. சிக்கலான சட்ட கணக்குலாவை எளிய சொற்களில் விளக்குவது
4. முக்கிய சட்ட விதிகள் மற்றும் நடைமுறைகளை முறைப்படுத்துவது""",
}

# Query enhancement templates for different languages
QUERY_ENHANCEMENT_TEMPLATES: Dict[str, Dict[str, str]] = {
    'en': {
        'general': "Answer this legal question about Indian law: {query}",
        'scenario': "Analyze this legal scenario under Indian law: {query}",
        'section': "Explain Section {number} of {act}: {query}",
        'case': "Provide information about the legal case: {query}",
        'procedure': "Explain the legal procedure for: {query}",
    },
    'hi': {
        'general': "भारतीय कानून के बारे में इस कानूनी प्रश्न का उत्तर दें: {query}",
        'scenario': "भारतीय कानून के तहत इस कानूनी परिस्थिति का विश्लेषण करें: {query}",
        'section': "भारतीय दंड संहिता की धारा {number} की व्याख्या करें: {query}",
        'case': "कानूनी मामले के बारे में जानकारी प्रदान करें: {query}",
        'procedure': "निम्नलिखित के लिए कानूनी प्रक्रिया की व्याख्या करें: {query}",
    },
    'bn': {
        'general': "ভারতীয় আইন সম্পর্কে এই আইনী প্রশ্নের উত্তর দিন: {query}",
        'scenario': "ভারতীয় আইনের অধীনে এই আইনী পরিস্থিতি বিশ্লেষণ করুন: {query}",
        'section': "ভারতীয় দণ্ড সংহিতার ধারা {number} ব্যাখ্যা করুন: {query}",
        'case': "আইনী মামলা সম্পর্কে তথ্য প্রদান করুন: {query}",
        'procedure': "নিম্নলিখিত আইনী পদ্ধতি ব্যাখ্যা করুন: {query}",
    },
}

# Context-aware legal terminology mappings
LEGAL_CONTEXT_MAPPINGS: Dict[str, Dict[str, List[str]]] = {
    'en': {
        'crime_related': ['theft', 'murder', 'assault', 'fraud', 'rape', 'offense', 'crime', 'criminal'],
        'procedure_related': ['bail', 'appeal', 'petition', 'filing', 'summons', 'charge', 'trial'],
        'civil': ['contract', 'dispute', 'compensation', 'lawsuit', 'plaintiff', 'defendant'],
        'family': ['divorce', 'marriage', 'custody', 'alimony', 'domestic', 'spouse'],
        'property': ['property', 'land', 'deed', 'ownership', 'lease', 'tenant', 'landlord'],
    },
    'hi': {
        'crime_related': ['चोरी', 'हत्या', 'हमला', 'धोखाधड़ी', 'बलात्कार', 'अपराध', 'अपराधी'],
        'procedure_related': ['जमानत', 'अपील', 'याचिका', 'आवेदन', 'समन', 'आरोप', 'मुकदमा'],
        'civil': ['अनुबंध', 'विवाद', 'मुआवजा', 'मुकदमा', 'वादी', 'प्रतिवादी'],
        'family': ['तलाक', 'विवाह', 'हिरासत', 'गुजारा', 'घरेलू', 'पति/पत्नी'],
        'property': ['संपत्ति', 'जमीन', 'विलेख', 'स्वामित्व', 'लीज', 'किरायेदार', 'मकान मालिक'],
    },
}

# Response formatting templates
RESPONSE_FORMAT_TEMPLATES: Dict[str, Dict[str, str]] = {
    'en': {
        'section_explanation': "**Section {section_num}**: {title}\n\n{explanation}\n\n**Punishment**: {punishment}",
        'scenario_analysis': "**Scenario Analysis**\n\n**Facts**: {facts}\n\n**Applicable Law**: {law}\n\n**Analysis**: {analysis}\n\n**Conclusion**: {conclusion}",
        'procedure_steps': "**Legal Procedure for {topic}**\n\n{steps}",
        'sources': "**Source Documents**\n\n{sources}",
    },
    'hi': {
        'section_explanation': "**धारा {section_num}**: {title}\n\n{explanation}\n\n**सजा**: {punishment}",
        'scenario_analysis': "**परिस्थिति विश्लेषण**\n\n**तथ्य**: {facts}\n\n**लागू कानून**: {law}\n\n**विश्लेषण**: {analysis}\n\n**निष्कर्ष**: {conclusion}",
        'procedure_steps': "**{topic} के लिए कानूनी प्रक्रिया**\n\n{steps}",
        'sources': "**स्रोत दस्तावेज़**\n\n{sources}",
    },
}


class LanguageSpecificPromptManager:
    """Manages language-specific prompts and context"""

    def __init__(self):
        """Initialize the prompt manager"""
        self.system_prompts = SYSTEM_PROMPTS
        self.query_templates = QUERY_ENHANCEMENT_TEMPLATES
        self.context_mappings = LEGAL_CONTEXT_MAPPINGS
        self.response_formats = RESPONSE_FORMAT_TEMPLATES

    def get_system_prompt(self, language_code: str) -> str:
        """
        Get system prompt for a language
        
        Args:
            language_code: Language code (e.g., 'en', 'hi', 'bn', 'ta')
            
        Returns:
            System prompt string
        """
        return self.system_prompts.get(language_code, self.system_prompts['en'])

    def enhance_query(
        self,
        query: str,
        language_code: str = 'en',
        query_type: str = 'general'
    ) -> str:
        """
        Enhance a query with language-specific context
        
        Args:
            query: Original query
            language_code: Language code
            query_type: Type of query (general, scenario, section, case, procedure)
            
        Returns:
            Enhanced query string
        """
        templates = self.query_templates.get(language_code, self.query_templates['en'])
        template = templates.get(query_type, templates.get('general'))

        try:
            return template.format(query=query, number='', act='')
        except Exception:
            return query

    def get_legal_context(
        self,
        query: str,
        language_code: str = 'en'
    ) -> Dict[str, List[str]]:
        """
        Get legal context for a query
        
        Args:
            query: Query string
            language_code: Language code
            
        Returns:
            Dictionary with identified legal contexts
        """
        contexts = self.context_mappings.get(language_code, self.context_mappings['en'])
        query_lower = query.lower()

        identified_contexts = {}
        for context_type, keywords in contexts.items():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    if context_type not in identified_contexts:
                        identified_contexts[context_type] = []
                    identified_contexts[context_type].append(keyword)

        return identified_contexts

    def format_response(
        self,
        response_type: str,
        language_code: str = 'en',
        **kwargs
    ) -> str:
        """
        Format a response according to language-specific template
        
        Args:
            response_type: Type of response (section_explanation, scenario_analysis, etc.)
            language_code: Language code
            **kwargs: Format variables
            
        Returns:
            Formatted response string
        """
        formats = self.response_formats.get(language_code, self.response_formats['en'])
        template = formats.get(response_type, "")

        try:
            return template.format(**kwargs)
        except Exception as e:
            return f"Error formatting response: {e}"

    def translate_legal_term(
        self,
        term: str,
        from_language: str = 'en',
        to_language: str = 'en'
    ) -> Optional[str]:
        """
        Translate a legal term between languages
        
        Args:
            term: Legal term to translate
            from_language: Source language code
            to_language: Target language code
            
        Returns:
            Translated term or None
        """
        # Try to find in context mappings
        if from_language in LEGAL_CONTEXT_MAPPINGS:
            for context_type, keywords in LEGAL_CONTEXT_MAPPINGS[from_language].items():
                if term.lower() in [k.lower() for k in keywords]:
                    idx = [k.lower() for k in keywords].index(term.lower())
                    target_keywords = LEGAL_CONTEXT_MAPPINGS.get(
                        to_language,
                        LEGAL_CONTEXT_MAPPINGS['en']
                    )[context_type]
                    if idx < len(target_keywords):
                        return target_keywords[idx]
        return None

    def get_language_specific_tips(self, language_code: str) -> List[str]:
        """Get language-specific tips for users"""
        tips = {
            'en': [
                "Be specific in your questions - mention the act or section if you know it",
                "Provide context - explain the scenario or situation",
                "Ask follow-up questions if something is unclear",
                "Use terms like 'Section X IPC' or 'Article Y Constitution' for precision"
            ],
            'hi': [
                "अपने प्रश्न में विशिष्ट रहें - यदि आप जानते हैं तो अधिनियम या धारा का उल्लेख करें",
                "संदर्भ प्रदान करें - परिस्थिति या स्थिति की व्याख्या करें",
                "यदि कोई बात स्पष्ट न हो तो अनुवर्ती प्रश्न पूछें",
                "'धारा X IPC' या 'अनुच्छेद Y संविधान' जैसे शब्दों का उपयोग करें"
            ],
            'bn': [
                "আপনার প্রশ্নে নির্দিষ্ট হন - যদি জানেন তাহলে আইন বা ধারা উল্লেখ করুন",
                "প্রসঙ্গ প্রদান করুন - পরিস্থিতি বা অবস্থার ব্যাখ্যা করুন",
                "যদি কিছু অস্পষ্ট হয় তবে অনুসরণ প্রশ্ন জিজ্ঞাসা করুন",
                "নির্ভুলতার জন্য 'ধারা X আইপিসি' বা 'অনুচ্ছেদ Y সংবিধান' এর মতো শর্তাবলী ব্যবহার করুন"
            ],
        }
        return tips.get(language_code, tips.get('en', []))


# Singleton instance
_prompt_manager_instance = None


def get_prompt_manager() -> LanguageSpecificPromptManager:
    """Get or create the prompt manager singleton"""
    global _prompt_manager_instance
    if _prompt_manager_instance is None:
        _prompt_manager_instance = LanguageSpecificPromptManager()
    return _prompt_manager_instance


def get_system_prompt(language_code: str = 'en') -> str:
    """Convenience function to get system prompt"""
    manager = get_prompt_manager()
    return manager.get_system_prompt(language_code)


def enhance_query_for_language(
    query: str,
    language_code: str = 'en',
    query_type: str = 'general'
) -> str:
    """Convenience function to enhance query"""
    manager = get_prompt_manager()
    return manager.enhance_query(query, language_code, query_type)
