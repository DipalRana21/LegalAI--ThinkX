# ⚖️ NyayaSahayak - AI Legal Assistant
### A RAG-based Intelligent Legal Advisor for the New BNS 2023 Laws

**NyayaSahayak** is an advanced AI prototype designed to democratize legal knowledge. It uses Retrieval-Augmented Generation (RAG) to provide accurate, citation-backed answers from the *Bharatiya Nyaya Sanhita (BNS) 2023*, ensuring zero hallucinations.

---

## 🌟 Key Features
- **📜 Zero Hallucinations:** Answers are strictly grounded in the uploaded BNS PDF.
- **🔍 Smart Citations:** Provides exact section numbers and displays the "Evidence Card" from the legal text.
- **⚡ Local Vector Search:** Uses ChromaDB for instant retrieval without internet dependency for search.
- **🎨 Cyber-Legal UI:** A modern, dark-themed interface designed for professional use.

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Custom CSS)
- **AI Model:** Google Gemini Pro (via LangChain)
- **Vector DB:** ChromaDB
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **Orchestration:** LangChain Core

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key

### 2. Installation
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO.git](https://github.com/YOUR_USERNAME/YOUR_REPO.git)
cd LegalAI
pip install -r requirements.txt
