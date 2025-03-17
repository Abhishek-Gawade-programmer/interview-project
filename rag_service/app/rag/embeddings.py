from typing import List, Dict, Any
import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.core.config import settings


class EmbeddingManager:
    """Manages document embeddings using Langchain with OpenAI embeddings"""
    
    def __init__(self):
        """Initialize the embedding manager with OpenAI embeddings"""
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Set up persistent DB path
        self.persist_directory = os.path.join(settings.UPLOAD_FOLDER, "chroma_db")
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize vector store
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
    
    def create_document_embeddings(self, chunks: List[str], document_id: int) -> List[str]:
        """
        Create embeddings for document chunks and store them in the vector store.
        
        Args:
            chunks: List of text chunks from the document
            document_id: The ID of the document
            
        Returns:
            List of embedding IDs for each chunk
        """
        # Create Langchain documents with metadata
        langchain_docs = [
            LangchainDocument(
                page_content=chunk,
                metadata={"document_id": document_id, "chunk_index": i}
            )
            for i, chunk in enumerate(chunks)
        ]
        
        # Add documents to the vector store
        ids = [f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))]
        self.vector_store.add_documents(langchain_docs, ids=ids)
        
        # Persist the vector store
        self.vector_store.persist()
        
        return ids
    
    def search_similar_chunks(self, query: str, document_id: int = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for chunks similar to the query.
        
        Args:
            query: The query text
            document_id: Optional document ID to filter results
            top_k: Number of results to return
            
        Returns:
            List of dictionaries containing chunk content and metadata
        """
        # Default search
        if document_id is None:
            results = self.vector_store.similarity_search_with_score(query, k=top_k)
        else:
            # Filter by document ID
            results = self.vector_store.similarity_search_with_score(
                query, 
                k=top_k,
                filter={"document_id": document_id}
            )
        
        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
        
        return formatted_results


# Create a global instance
embedding_manager = EmbeddingManager() 