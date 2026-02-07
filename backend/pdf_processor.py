"""
PDF Processing Module
Handles PDF loading, text extraction, and chunking for RAG system
"""

import os
from typing import List
from pypdf import PdfReader
from langchain_core.documents import Document


class PDFProcessor:
    """Processes PDF files and converts them into document chunks"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._text_splitter = None
    
    @property
    def text_splitter(self):
        """Lazy load text splitter to avoid importing heavy dependencies"""
        if self._text_splitter is None:
            try:
                # Import only when needed to avoid TensorFlow/transformers compatibility issues
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                self._text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap,
                    length_function=len,
                    separators=["\n\n", "\n", ". ", " ", ""]
                )
            except Exception as e:
                # Fallback: use a simple text splitter if langchain_text_splitters fails
                print(f"Warning: Could not import RecursiveCharacterTextSplitter: {e}")
                print("Using simple text splitter as fallback...")
                # Simple fallback splitter
                class SimpleTextSplitter:
                    def __init__(self, chunk_size, chunk_overlap):
                        self.chunk_size = chunk_size
                        self.chunk_overlap = chunk_overlap
                    
                    def split_text(self, text):
                        chunks = []
                        start = 0
                        while start < len(text):
                            end = start + self.chunk_size
                            chunk = text[start:end]
                            chunks.append(chunk)
                            start = end - self.chunk_overlap
                        return chunks
                
                self._text_splitter = SimpleTextSplitter(
                    self.chunk_size,
                    self.chunk_overlap
                )
        return self._text_splitter
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {str(e)}")
            return ""
    
    def process_pdf(self, pdf_path: str) -> List[Document]:
        """Process a PDF file and return document chunks"""
        print(f"Processing PDF: {pdf_path}")
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text.strip():
            print(f"Warning: No text extracted from {pdf_path}")
            return []
        
        # Create documents with metadata
        documents = []
        chunks = self.text_splitter.split_text(text)
        
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": os.path.basename(pdf_path),
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            )
            documents.append(doc)
        
        print(f"Created {len(documents)} chunks from {pdf_path}")
        return documents
    
    def process_multiple_pdfs(self, pdf_paths: List[str]) -> List[Document]:
        """Process multiple PDF files and return combined document chunks"""
        all_documents = []
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                documents = self.process_pdf(pdf_path)
                all_documents.extend(documents)
            else:
                print(f"Warning: PDF file not found: {pdf_path}")
        
        print(f"Total documents processed: {len(all_documents)}")
        return all_documents

