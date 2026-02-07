import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for accessing PDF files
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# PDF Configuration - PDFs are in project root
PDF_DIRECTORY = "data"
# PDF file paths (use absolute paths or relative paths from project root)
PDF_FILES = [
    r"E:\SEM-6\Hack\250883_english_01042024.pdf",  # Main legal document
    # Add more PDF files here if needed
    # r"E:\SEM-6\Hack\BNS2023.pdf",
]
# Convert relative paths to absolute paths and verify files exist
valid_pdf_files = []
for pdf_path in PDF_FILES:
    if os.path.isabs(pdf_path):
        abs_path = pdf_path
    else:
        abs_path = os.path.join(parent_dir, pdf_path)
    
    if os.path.exists(abs_path):
        valid_pdf_files.append(abs_path)
    else:
        print(f"Warning: PDF file not found: {abs_path}")

PDF_FILES = valid_pdf_files

# Vector Store Configuration
VECTOR_STORE_PATH = os.path.join(parent_dir, "vector_store")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# LLM Configuration
MODEL_NAME = "gemini-2.5-flash"
TEMPERATURE = 0.3
MAX_TOKENS = 2048

# RAG Configuration
TOP_K_RESULTS = 5

