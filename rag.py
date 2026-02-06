import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ⚠️ PASTE YOUR KEY HERE
os.environ["GOOGLE_API_KEY"] = "AIzaSyAlHWmiBT6sT-oTnN6sAM-5soNjayfXOd8"

def get_answer(query):
    # 1. Connect to Database
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory="legal_db", embedding_function=embeddings)
    
    # 2. Setup Retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # 3. Retrieve Documents Manually
    docs = retriever.invoke(query)
    
    # 4. Format Context
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # 5. Define the Prompt (We force the legal persona here)
    template = """
    You are an expert Indian Legal Assistant. Use the following context from the BNS 2023 laws to answer the question.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer clearly and cite the section number if available:
    """
    
    prompt = PromptTemplate.from_template(template)
    
    # 6. Setup LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # 7. Generate Answer
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"context": context_text, "question": query})
    
    # Return in the format app.py expects
    return {
        "result": result,
        "source_documents": docs
    }