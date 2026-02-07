"""
RAG Chain Module
Handles the RAG pipeline with LangChain and Google Gemini
"""

import os

# Disable TensorFlow before any imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['DISABLE_TF'] = '1'

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
except ImportError as e:
    raise ImportError(f"Failed to import LangChain modules: {e}")

# Import these after LangChain to avoid triggering TensorFlow imports
try:
    from .vector_store import VectorStoreManager
except ImportError as e:
    raise ImportError(f"Failed to import VectorStoreManager: {e}")

try:
    from . import config
except ImportError as e:
    raise ImportError(f"Failed to import config: {e}")


class RAGChain:
    """RAG Chain for legal query answering"""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store_manager = vector_store_manager
        
        # Initialize LLM
        if not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model=config.MODEL_NAME,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS
        )
        
        # Custom prompt for legal assistance
        self.prompt_template = """You are an intelligent legal assistant specializing in Indian laws and legal provisions. 
Your task is to help users understand legal information in a clear, simplified manner.

Context from legal documents:
{context}

User Question: {question}

Instructions:
1. Answer the question based ONLY on the provided context from Indian legal documents
2. If the answer is not in the context, clearly state that the information is not available in the provided documents
3. Explain legal terms in simple, understandable language
4. Cite the source document when referencing specific laws or acts
5. If relevant, mention section numbers, act names, or amendment details
6. Keep the response concise but comprehensive
7. Use bullet points or numbered lists for clarity when appropriate

Answer:"""
        
        self.prompt = PromptTemplate.from_template(self.prompt_template)
        
        # Create RAG chain
        self.qa_chain = None
        self._initialize_chain()
    
    def _initialize_chain(self):
        """Initialize the RAG chain using LangChain 1.x API"""
        retriever = self.vector_store_manager.get_retriever(k=config.TOP_K_RESULTS)
        
        # Create RAG chain using LangChain 1.x style
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        # Build the chain
        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        self.qa_chain = rag_chain
        self.retriever = retriever  # Store retriever for source documents
    
    def query(self, question: str) -> dict:
        """Query the RAG system"""
        if self.qa_chain is None:
            raise ValueError("RAG chain not initialized")
        
        try:
            # Get answer from chain
            answer = self.qa_chain.invoke(question)
            
            # Get source documents
            source_documents = self.retriever.invoke(question)
            
            return {
                "answer": answer,
                "source_documents": source_documents
            }
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "source_documents": []
            }

# Explicitly export RAGChain
__all__ = ['RAGChain']

