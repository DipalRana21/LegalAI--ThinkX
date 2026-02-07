"""
Vector Store Module
Handles FAISS vector store creation, loading, and similarity search
"""

import os
import sys
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Disable TensorFlow before importing transformers-dependent modules
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['DISABLE_TF'] = '1'

# Patch importlib.util.find_spec to prevent TensorFlow detection
import importlib.util

# Save original find_spec if not already patched
if not hasattr(importlib.util, '_original_find_spec'):
    importlib.util._original_find_spec = importlib.util.find_spec
    
    def patched_find_spec(name, package=None):
        """Patched find_spec that returns None for tensorflow"""
        if name == 'tensorflow' or (isinstance(name, str) and name.startswith('tensorflow')):
            return None  # Pretend tensorflow doesn't exist
        return importlib.util._original_find_spec(name, package)
    
    # Monkey patch find_spec
    importlib.util.find_spec = patched_find_spec


class VectorStoreManager:
    """Manages FAISS vector store for document embeddings"""
    
    def __init__(self, store_path: str = "vector_store"):
        self.store_path = store_path
        self._embeddings = None  # Lazy initialization
        self.vector_store = None
    
    @property
    def embeddings(self):
        """Lazy load embeddings model only when needed"""
        if self._embeddings is None:
            print("Loading embeddings model (this may take a moment on first run)...")
            try:
                # Suppress warnings during import
                import warnings
                warnings.filterwarnings("ignore")
                
                # Try to use HuggingFace embeddings
                from langchain_community.embeddings import HuggingFaceEmbeddings
                self._embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
                print("✓ Embeddings model loaded successfully")
            except ImportError as e:
                error_msg = str(e)
                if "is_torch_less_than_1_11" in error_msg or "pytorch_utils" in error_msg:
                    print("ERROR: Transformers/Torch version compatibility issue detected!")
                    print("\nPlease run the fix script:")
                    print("  python fix_dependencies.py")
                    print("\nOr manually fix with:")
                    print("  pip uninstall transformers tokenizers sentence-transformers -y")
                    print("  pip install transformers>=4.40.0 tokenizers>=0.19.0,<0.22.0")
                    raise RuntimeError(
                        "Transformers version incompatibility. "
                        "Run: python fix_dependencies.py"
                    )
                else:
                    print(f"Warning: Could not load HuggingFace embeddings: {e}")
                    raise
            except Exception as e:
                print(f"ERROR: Could not load embedding model: {e}")
                print("\nTroubleshooting:")
                print("1. Run: python fix_dependencies.py")
                print("2. Or: pip install --upgrade sentence-transformers transformers torch")
                raise RuntimeError(
                    f"Failed to load embedding model: {e}\n"
                    "Try running: python fix_dependencies.py"
                )
        return self._embeddings
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """Create a new FAISS vector store from documents"""
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        print("Creating vector store...")
        print(f"Embedding {len(documents)} documents...")
        
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        print("Vector store created successfully!")
        return self.vector_store
    
    def save_vector_store(self):
        """Save the vector store to disk"""
        if self.vector_store is None:
            raise ValueError("No vector store to save")
        
        os.makedirs(self.store_path, exist_ok=True)
        self.vector_store.save_local(self.store_path)
        print(f"Vector store saved to {self.store_path}")
    
    def load_vector_store(self) -> FAISS:
        """Load vector store from disk"""
        if not os.path.exists(self.store_path):
            raise FileNotFoundError(f"Vector store not found at {self.store_path}")
        
        print(f"Loading vector store from {self.store_path}...")
        self.vector_store = FAISS.load_local(
            self.store_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print("Vector store loaded successfully!")
        return self.vector_store
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Perform similarity search on the vector store"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results
    
    def get_retriever(self, k: int = 5):
        """Get a retriever from the vector store"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )

