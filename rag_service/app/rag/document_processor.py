import os
import re
from typing import List, Dict, Any
import uuid

from app.core.config import settings


class DocumentProcessor:
    """
    Process documents for the RAG pipeline, including:
    - Document loading
    - Text extraction
    - Text chunking
    - File management
    """
    
    def __init__(self):
        # Create upload folder if it doesn't exist
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    
    def save_uploaded_file(self, file, user_id: int) -> str:
        """Save the uploaded file to disk."""
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_FOLDER, filename)
        
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        return file_path
    
    def load_document(self, file_path: str, file_type: str) -> str:
        """Load and extract text from a document file."""
        # In a real implementation, we would use specialized loaders like PyPDFLoader, etc.
        # For simplicity, we'll just read the file as text
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        return text
    
    def split_text_into_chunks(self, text: str) -> List[str]:
        """Split the text into smaller chunks for processing."""
        # Simple implementation: split by paragraphs
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Filter out empty paragraphs and trim
        chunks = [p.strip() for p in paragraphs if p.strip()]
        
        # Combine short paragraphs
        result = []
        current_chunk = ""
        
        for chunk in chunks:
            if len(current_chunk) + len(chunk) < 1000:
                current_chunk += "\n\n" + chunk if current_chunk else chunk
            else:
                if current_chunk:
                    result.append(current_chunk)
                current_chunk = chunk
        
        if current_chunk:
            result.append(current_chunk)
        
        return result
    
    def detect_file_type(self, filename: str) -> str:
        """Detect the file type from the filename."""
        extension = filename.lower().split(".")[-1]
        if extension in ["pdf"]:
            return "pdf"
        elif extension in ["txt", "text"]:
            return "txt"
        elif extension in ["docx", "doc"]:
            return "docx"
        elif extension in ["html", "htm"]:
            return "html"
        else:
            return "txt"  # Default to text
    
    def preprocess_document(self, file_path: str, file_type: str) -> List[str]:
        """Load the document and split it into chunks."""
        text = self.load_document(file_path, file_type)
        chunks = self.split_text_into_chunks(text)
        return chunks


# Create a global instance
document_processor = DocumentProcessor() 