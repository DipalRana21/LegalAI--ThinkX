import streamlit as st

st.set_page_config(
    page_title="🇮🇳 Personal Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("🇮🇳 Personal Legal Assistant")
st.markdown("*Your AI-powered guide to Indian laws and citizen rights*")

# Simple Legal Assistant (Demo Version)
class SimpleLegalAssistant:
    def __init__(self):
        # Legal knowledge base
        self.legal_db = {
            "ipc 420": {
                "section": "IPC 420 - Cheating",
                "punishment": "Up to 7 years imprisonment + fine",
                "rights": "Right to legal representation, bail application, appeal within 30 days",
                "procedure": "Must be produced before magistrate within 24 hours"
            },
            "arrest": {
                "section": "CrPC Section 50, 41, 41A",
                "rights": "Right to know grounds of arrest, legal aid, inform family, no torture",
                "procedure": "Must be informed of grounds, can contact lawyer immediately",
                "timeline": "Produced before magistrate within 24 hours"
            },
            "bail": {
                "section": "CrPC Section 437, 439",
                "rights": "Right to bail application, legal representation during hearings",
                "factors": "Court considers flight risk, evidence tampering",
                "types": "Regular bail, anticipatory bail available"
            },
            "consumer": {
                "section": "Consumer Protection Act 2019",
                "rights": "File complaint in consumer forum, compensation for deficiency",
                "procedure": "Can approach district/state/national consumer forum",
                "remedies": "Refund, replacement, compensation"
            },
            "domestic violence": {
                "section": "Protection of Women from Domestic Violence Act 2005",
                "rights": "Protection order, residence order, maintenance",
                "procedure": "Approach magistrate, can get immediate relief",
                "support": "Free legal aid available"
            }
        }
    
    def get_legal_advice(self, query):
        query_lower = query.lower()
        
        # Match query to legal topics
        if any(term in query_lower for term in ["ipc 420", "cheating", "fraud"]):
            info = self.legal_db["ipc 420"]
            return f"""
**{info['section']}**

**Punishment:** {info['punishment']}

**Your Rights:**
- {info['rights']}
- {info['procedure']}

**What to do:** Immediately contact a lawyer, do not resist arrest, ask for grounds of arrest in writing.
            """, "Criminal Law - IPC 420"
            
        elif any(term in query_lower for term in ["arrest", "police", "custody"]):
            info = self.legal_db["arrest"]
            return f"""
**{info['section']} - Arrest Rights**

**Your Rights During Arrest:**
- {info['rights']}
- {info['procedure']}

**Timeline:** {info['timeline']}

**What to do:** Stay calm, ask for arrest memo, contact lawyer immediately, inform family.
            """, "Criminal Procedure - Arrest Rights"
            
        elif any(term in query_lower for term in ["bail", "release"]):
            info = self.legal_db["bail"]
            return f"""
**{info['section']} - Bail Provisions**

**Your Rights:**
- {info['rights']}

**Court Considerations:** {info['factors']}

**Types Available:** {info['types']}

**What to do:** File bail application through lawyer, provide surety, appear for hearings.
            """, "Criminal Procedure - Bail"
            
        elif any(term in query_lower for term in ["consumer", "purchase", "defective", "service"]):
            info = self.legal_db["consumer"]
            return f"""
**{info['section']}**

**Your Rights:**
- {info['rights']}

**Procedure:** {info['procedure']}

**Remedies Available:** {info['remedies']}

**What to do:** Keep all bills/receipts, approach consumer forum within 2 years, file complaint with evidence.
            """, "Consumer Rights"
            
        elif any(term in query_lower for term in ["domestic violence", "harassment", "protection"]):
            info = self.legal_db["domestic violence"]
            return f"""
**{info['section']}**

**Your Rights:**
- {info['rights']}

**Procedure:** {info['procedure']}

**Support:** {info['support']}

**What to do:** Document incidents, approach magistrate, contact women helpline 181, seek legal aid.
            """, "Women Rights - Domestic Violence"
            
        else:
            return """
I understand you have a legal question. Based on the query, here's general guidance:

**General Legal Rights:**
- Right to legal representation
- Right to fair trial
- Right to appeal
- Right to bail (in most cases)

**What to do:**
1. Consult a qualified lawyer immediately
2. Keep all relevant documents
3. Do not sign anything without legal advice
4. Know your constitutional rights

**Emergency Numbers:**
- Police: 100
- Women Helpline: 181
- Legal Aid: Contact your district legal services authority

**Remember:** This is general information only. Always consult a qualified lawyer for specific legal advice.
            """, "General Legal Guidance"

# Initialize assistant
assistant = SimpleLegalAssistant()

# Sidebar
st.sidebar.header("ℹ️ About")
st.sidebar.info("""
This Legal Assistant provides information about:
- Indian Penal Code (IPC)
- Criminal Procedure Code (CrPC)
- Consumer Protection Laws
- Women's Rights
- Arrest and Bail procedures
""")

st.sidebar.header("⚠️ Important Disclaimer")
st.sidebar.error("""
**FOR EDUCATIONAL PURPOSES ONLY**

This is NOT legal advice. Always consult a qualified lawyer for:
- Specific legal situations
- Court proceedings
- Legal document preparation
- Professional legal representation
""")

st.sidebar.header("📞 Emergency Contacts")
st.sidebar.info("""
- **Police Emergency:** 100
- **Women Helpline:** 181  
- **Legal Aid Helpline:** 15100
- **Child Helpline:** 1098
""")

# Main interface
st.subheader("💡 Ask Your Legal Question")

question = st.text_area(
    "Type your legal question here:",
    placeholder="e.g., What are my rights if arrested under IPC 420?",
    height=100
)

if st.button("🔍 Get Legal Information", type="primary"):
    if question.strip():
        with st.spinner("🔍 Analyzing your legal query..."):
            advice, category = assistant.get_legal_advice(question)
            
            st.success(f"**Category:** {category}")
            st.write(advice)
            
            st.info("💡 **Next Steps:** Consult a qualified lawyer for personalized legal advice specific to your situation.")
    else:
        st.warning("Please enter your legal question.")

# Sample questions
st.subheader("💡 Common Legal Questions")

sample_questions = [
    "What are my rights if arrested under IPC 420?",
    "How to file consumer complaint for defective product?", 
    "What are bail provisions in criminal cases?",
    "What rights do I have during police arrest?",
    "How to get protection from domestic violence?"
]

cols = st.columns(2)
for i, sample in enumerate(sample_questions):
    col_idx = i % 2
    if cols[col_idx].button(f"📝 {sample}", key=f"sample_{i}"):
        # Auto-fill the question
        st.session_state.selected_question = sample
        st.rerun()

# Display selected sample question
if 'selected_question' in st.session_state:
    st.text_area("Selected Question:", st.session_state.selected_question, key="auto_question")
    if st.button("🔍 Get Answer for Selected Question"):
        advice, category = assistant.get_legal_advice(st.session_state.selected_question)
        st.success(f"**Category:** {category}")
        st.write(advice)

# Legal Resources
st.subheader("📚 Helpful Legal Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **🏛️ Government Resources**
    - [India Code](https://www.indiacode.nic.in/)
    - [Supreme Court of India](https://main.sci.gov.in/)
    - [Legal Services Authority](https://nalsa.gov.in/)
    """)

with col2:
    st.info("""
    **👥 Legal Aid** 
    - District Legal Services Authority
    - Free legal aid for poor
    - Women's legal aid centres
    """)

with col3:
    st.info("""
    **📱 Helplines**
    - Police: 100
    - Women: 181
    - Legal Aid: 15100
    - Child: 1098
    """)

# Footer
st.markdown("---")
st.markdown("**🔴 IMPORTANT:** This tool provides general legal information only. Always consult qualified legal professionals for actual legal advice.")
st.markdown("*Built for educational purposes | Not a substitute for professional legal counsel*")