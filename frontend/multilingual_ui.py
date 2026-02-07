"""
Multilingual UI Component for Streamlit
Provides interactive language selection and switching components
"""

import streamlit as st
from typing import Optional, Dict, List, Tuple
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from backend.multilingual import (
    get_multilingual_processor,
    INDIAN_LANGUAGES,
)
from backend.language_strings import (
    get_string,
    get_all_strings,
    LANGUAGE_STRINGS,
)


class MultilingualUI:
    """Interactive UI component for multilingual support"""

    # CSS for styling
    MULTILINGUAL_CSS = """
    <style>
    .language-selector-container {
        background: linear-gradient(135deg, rgba(15, 52, 96, 0.05) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        border: 1px solid rgba(15, 52, 96, 0.1);
    }

    .language-tabs {
        display: flex;
        gap: 0.5rem;
        margin: 0.75rem 0;
        flex-wrap: wrap;
    }

    .language-tab {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 2px solid transparent;
        cursor: pointer;
        font-weight: 500;
        background: white;
        color: #0f3460;
        transition: all 0.3s ease;
        min-width: fit-content;
    }

    .language-tab:hover {
        background: #f1f5f9;
        border-color: #f59e0b;
        transform: translateY(-2px);
    }

    .language-tab-active {
        background: linear-gradient(135deg, #0f3460 0%, #1a4a7a 100%);
        color: white;
        border-color: #1a4a7a;
        box-shadow: 0 4px 12px rgba(15, 52, 96, 0.25);
    }

    .language-info {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-top: 0.75rem;
        font-size: 0.9rem;
        color: #92400e;
    }

    .language-flag {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }

    .voice-control-panel {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.05) 0%, rgba(100, 116, 139, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
        border: 1px solid #e2e8f0;
    }

    .response-language-selector {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(248, 113, 113, 0.05) 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
        border: 1px solid #fcd34d;
    }

    .language-stat {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: #f1f5f9;
        border-radius: 6px;
        margin-right: 0.5rem;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }

    .language-stat-value {
        font-weight: 600;
        color: #0f3460;
    }
    </style>
    """

    def __init__(self):
        """Initialize the multilingual UI component"""
        self.processor = get_multilingual_processor()
        self._init_session_state()

    def _init_session_state(self) -> None:
        """Initialize session state for language preferences"""
        if 'user_language' not in st.session_state:
            st.session_state.user_language = 'english'
        if 'voice_language' not in st.session_state:
            st.session_state.voice_language = 'english'
        if 'response_language' not in st.session_state:
            st.session_state.response_language = 'english'
        if 'translation_enabled' not in st.session_state:
            st.session_state.translation_enabled = False
        if 'rtl_mode' not in st.session_state:
            st.session_state.rtl_mode = False

    def render_css(self) -> None:
        """Render CSS styling"""
        st.markdown(self.MULTILINGUAL_CSS, unsafe_allow_html=True)

    def render_language_selector(self) -> str:
        """
        Render main language selector UI
        
        Returns:
            Selected language key
        """
        st.markdown("### 🌐 Language Settings", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="language-selector-container">', unsafe_allow_html=True)

            # Main language selection
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("**Select Your Preferred Language**")
                
                # Get all language options - directly from INDIAN_LANGUAGES
                all_langs = list(INDIAN_LANGUAGES.keys())
                
                selected_lang = st.selectbox(
                    label="Choose Language",
                    options=all_langs,
                    format_func=lambda x: f"{INDIAN_LANGUAGES[x]['flag']} {INDIAN_LANGUAGES[x]['name']}",
                    index=all_langs.index(st.session_state.user_language) if st.session_state.user_language in all_langs else 0,
                    key="main_language_selector",
                    help="Select your preferred language for the interface",
                    label_visibility="collapsed"
                )

                if selected_lang != st.session_state.user_language:
                    st.session_state.user_language = selected_lang
                    st.rerun()

            with col2:
                lang_info = INDIAN_LANGUAGES.get(selected_lang, {})
                flag = lang_info.get('flag', '🌐')
                st.markdown(f"<div style='font-size: 2rem; text-align: center; padding-top: 1rem;'>{flag}</div>", 
                          unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        return selected_lang

    def render_voice_input_selector(self) -> str:
        """
        Render voice input language selector
        
        Returns:
            Selected voice language key
        """
        st.markdown("### 🎤 Voice Input Settings (12 Languages)", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="voice-control-panel">', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            all_langs = list(INDIAN_LANGUAGES.keys())
            with col1:
                st.markdown("**Select Voice Input Language**")
                voice_lang = st.selectbox(
                    label="Voice Language",
                    options=all_langs,
                    format_func=lambda x: f"{INDIAN_LANGUAGES[x]['flag']} {INDIAN_LANGUAGES[x]['name']}",
                    index=all_langs.index(st.session_state.voice_language) if st.session_state.voice_language in all_langs else 0,
                    key="voice_language_selector",
                    help="Choose language for voice input",
                    label_visibility="collapsed"
                )
                st.session_state.voice_language = voice_lang

            with col2:
                st.markdown("**Voice Code**")
                voice_code = self.processor.get_voice_code_for_language(voice_lang)
                st.info(f"🔊 {voice_code}")

            # Voice input help
            st.markdown('<div class="language-info">', unsafe_allow_html=True)
            st.markdown(
                f"💡 Speak in {INDIAN_LANGUAGES[voice_lang]['name']} "
                f"({INDIAN_LANGUAGES[voice_lang]['flag']}). "
                "Click the microphone button and speak clearly.",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        return voice_lang

    def render_response_language_selector(self) -> str:
        """
        Render response language selector
        
        Returns:
            Selected response language key
        """
        st.markdown("### 💬 Response Language Settings (12 Languages)", unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="response-language-selector">', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            all_langs = list(INDIAN_LANGUAGES.keys())
            with col1:
                st.markdown("**Get Responses In**")
                response_lang = st.selectbox(
                    label="Response Language",
                    options=all_langs,
                    format_func=lambda x: f"{INDIAN_LANGUAGES[x]['flag']} {INDIAN_LANGUAGES[x]['name']}",
                    index=all_langs.index(st.session_state.response_language) if st.session_state.response_language in all_langs else 0,
                    key="response_language_selector",
                    help="Choose language for responses",
                    label_visibility="collapsed"
                )
                st.session_state.response_language = response_lang

            with col2:
                lang_info = INDIAN_LANGUAGES[response_lang]
                st.markdown("**Language Info**")
                st.metric(
                    label="Selected",
                    value=lang_info['flag'],
                    delta=lang_info['native_name']
                )

            # Show RTL warning if needed
            if lang_info.get('is_rtl'):
                st.warning(f"⚠️ RTL Mode: {lang_info['name']} uses right-to-left text direction")
                st.session_state.rtl_mode = True
            else:
                st.session_state.rtl_mode = False

            st.markdown('</div>', unsafe_allow_html=True)

        return response_lang

    def render_language_tabs(self, languages: Optional[List[str]] = None) -> str:
        """
        Render quick language tabs
        
        Args:
            languages: List of language keys to display
            
        Returns:
            Selected language key
        """
        if languages is None:
            languages = ['english', 'hindi', 'bengali', 'tamil', 'telugu']

        st.markdown("**Quick Language Switch**")
        
        cols = st.columns(len(languages))
        selected = st.session_state.user_language

        for idx, col in enumerate(cols):
            with col:
                lang_key = languages[idx]
                lang_info = INDIAN_LANGUAGES.get(lang_key, {})
                flag = lang_info.get('flag', '🌐')
                name = lang_info.get('code', '').upper()

                is_selected = lang_key == selected
                button_style = "language-tab language-tab-active" if is_selected else "language-tab"

                if st.button(
                    f"{flag} {name}",
                    key=f"quick_lang_{lang_key}",
                    use_container_width=True,
                ):
                    st.session_state.user_language = lang_key
                    st.rerun()

        return selected

    def render_translation_options(self) -> Dict[str, bool]:
        """
        Render translation options
        
        Returns:
            Dictionary with translation settings
        """
        st.markdown("### ⚙️ Translation Options", unsafe_allow_html=True)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                enable_translation = st.checkbox(
                    "🔄 Enable Auto-Translation",
                    value=st.session_state.translation_enabled,
                    help="Automatically translate responses to selected language"
                )
                st.session_state.translation_enabled = enable_translation

            with col2:
                show_original = st.checkbox(
                    "📝 Show Original Text",
                    value=False,
                    help="Display original text alongside translation"
                )

        return {
            'translation_enabled': enable_translation,
            'show_original': show_original
        }

    def translate_response(
        self,
        text: str,
        target_lang: str
    ) -> Tuple[str, bool]:
        """
        Translate response text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language key
            
        Returns:
            Tuple of (translated_text, translation_success)
        """
        lang_info = INDIAN_LANGUAGES.get(target_lang)
        if not lang_info:
            return text, False

        target_code = lang_info['code']

        # Don't translate if source and target are the same
        if target_code == 'en':
            return text, False

        translated, success = self.processor.translate_text(
            text,
            source_lang='en',
            target_lang=target_code
        )

        return translated, success

    def render_language_stats(self) -> None:
        """Render system language statistics and info"""
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Languages",
                len(INDIAN_LANGUAGES),
                "Supported"
            )

        with col2:
            st.metric(
                "Voice Input",
                "Available",
                INDIAN_LANGUAGES[st.session_state.voice_language]['flag']
            )

        with col3:
            st.metric(
                "Response Language",
                INDIAN_LANGUAGES[st.session_state.response_language]['code'].upper(),
                INDIAN_LANGUAGES[st.session_state.response_language]['flag']
            )

    def render_language_info_panel(self) -> None:
        """Render information panel about selected language"""
        lang_key = st.session_state.user_language
        lang_info = INDIAN_LANGUAGES.get(lang_key, {})

        if not lang_info:
            return

        with st.expander("ℹ️ Language Information"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Language Details**")
                st.markdown(f"- **Name**: {lang_info['name']}")
                st.markdown(f"- **Native**: {lang_info['native_name']}")
                st.markdown(f"- **Code**: {lang_info['code']}")
                st.markdown(f"- **Voice Code**: {lang_info['voice_code']}")

            with col2:
                st.write("**Properties**")
                st.markdown(f"- **Flag**: {lang_info['flag']}")
                st.markdown(f"- **RTL**: {'Yes' if lang_info.get('is_rtl') else 'No'}")
                st.markdown(f"- **Supported**: {'✓' if lang_info.get('supported') else '✗'}")
                st.markdown(f"- **Status**: Available")

    @staticmethod
    def _get_language_options() -> List[Tuple[str, str]]:
        """Get formatted language options"""
        options = []
        for key, info in INDIAN_LANGUAGES.items():
            if info.get('supported'):
                display_name = f"{info['flag']} {info['name']}"
                options.append((display_name, key))
        return sorted(options, key=lambda x: x[1])

    @staticmethod
    def _get_display_name(lang_key: str) -> str:
        """Get display name for language"""
        lang_info = INDIAN_LANGUAGES.get(lang_key, {})
        flag = lang_info.get('flag', '🌐')
        name = lang_info.get('name', lang_key)
        return f"{flag} {name}"

    def get_localized_string(self, key: str, category: str = 'general') -> str:
        """Get localized string for current language"""
        lang = st.session_state.user_language
        lang_code = INDIAN_LANGUAGES.get(lang, {}).get('code', 'en')
        return get_string(key, lang_code, category)

    def render_voice_input_with_microphone(self):
        """
        Render integrated voice input section with microphone for selected language
        Requires: streamlit_mic_recorder extension
        
        Returns:
            Transcribed text or None
        """
        try:
            from streamlit_mic_recorder import speech_to_text
        except ImportError:
            st.warning(
                "🎤 Voice input requires: `pip install streamlit-mic-recorder`\n\n"
                "**Install it to use voice input features.**"
            )
            return None

        st.markdown("### 🎤 Voice Input (Microphone)")
        
        with st.container():
            st.markdown('<div class="voice-control-panel">', unsafe_allow_html=True)
            
            # Get selected voice language
            voice_lang = st.session_state.get('voice_language', 'english')
            voice_code = self.processor.get_voice_code_for_language(voice_lang)
            lang_name = INDIAN_LANGUAGES.get(voice_lang, {}).get('name', 'English')
            lang_flag = INDIAN_LANGUAGES.get(voice_lang, {}).get('flag', '🌐')
            
            # Display language and voice code
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Speaking in:** {lang_flag} {lang_name}")
            with col2:
                st.info(f"🔊 {voice_code}")
            
            # Microphone input button
            st.markdown("<br>", unsafe_allow_html=True)
            voice_text = speech_to_text(
                language=voice_code,
                start_prompt="🎤 Tap to Speak",
                stop_prompt="⏹️ Stop Recording",
                just_once=True,
                use_container_width=True,
                key="voice_recorder_main"
            )
            
            # Help text
            st.markdown(
                f"💡 **Speak in {lang_name}** ({lang_flag}). "
                f"Click the button above, speak clearly, and the system will transcribe your words.",
                unsafe_allow_html=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        return voice_text

    def render_emergency_contacts(self):
        """
        Render emergency contacts in the selected language
        """
        from backend.language_strings import EMERGENCY_CONTACTS
        
        st.markdown("### 📞 Emergency & Help Numbers")
        
        with st.container():
            # Get selected language and its emergency contacts
            selected_lang = st.session_state.get('user_language', 'english')
            lang_code = INDIAN_LANGUAGES.get(selected_lang, {}).get('code', 'en')
            
            emergency_data = EMERGENCY_CONTACTS.get(lang_code, EMERGENCY_CONTACTS.get('en', {}))
            
            # Create three columns for emergency contacts
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(
                    f"{emergency_data.get('police', '🚨 Police')}\n"
                    f"**{emergency_data.get('police_number', '100')}**"
                )
            
            with col2:
                st.warning(
                    f"{emergency_data.get('women_helpline', '👩 Women Helpline')}\n"
                    f"**{emergency_data.get('women_number', '181')}**"
                )
            
            with col3:
                st.success(
                    f"{emergency_data.get('legal_aid', '📋 Legal Aid')}\n"
                    f"**{emergency_data.get('legal_aid_number', '15100')}**"
                )


def render_multilingual_sidebar() -> Dict[str, str]:
    """
    Render complete multilingual settings in sidebar
    
    Returns:
        Dictionary with language settings
    """
    ui = MultilingualUI()
    ui.render_css()

    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🌍 Language & Accessibility")

        user_lang = ui.render_language_selector()
        voice_lang = ui.render_voice_input_selector()
        response_lang = ui.render_response_language_selector()

        translation_opts = ui.render_translation_options()

        st.markdown("---")
        ui.render_language_stats()

        st.markdown("---")
        ui.render_language_info_panel()

    return {
        'user_language': user_lang,
        'voice_language': voice_lang,
        'response_language': response_lang,
        **translation_opts
    }


def get_current_language_settings() -> Dict[str, str]:
    """Get current language settings from session state"""
    return {
        'user_language': st.session_state.get('user_language', 'english'),
        'voice_language': st.session_state.get('voice_language', 'english'),
        'response_language': st.session_state.get('response_language', 'english'),
        'translation_enabled': st.session_state.get('translation_enabled', False),
        'rtl_mode': st.session_state.get('rtl_mode', False),
    }
