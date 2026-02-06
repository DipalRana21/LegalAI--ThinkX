import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- CONFIG ---
PDF_NAME = "bns_2024.pdf"
VECTOR_STORE_NAME = "legal_db"

def ingest():
    if not os.path.exists(PDF_NAME):
        print(f"❌ ERROR: {PDF_NAME} not found! Put it in the same folder.")
        return

    print("📄 1. Loading PDF...")
    loader = PyPDFLoader(PDF_NAME)
    docs = loader.load()
    print(f"   ✅ Loaded {len(docs)} pages.")

    print("✂️ 2. Splitting text...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    print(f"   ✅ Created {len(chunks)} chunks.")

    print("🧠 3. Creating Embeddings (This takes time)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("💾 4. Saving to Database...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_NAME
    )
    print("🎉 SUCCESS! Database created in 'legal_db' folder.")

if __name__ == "__main__":
    ingest()