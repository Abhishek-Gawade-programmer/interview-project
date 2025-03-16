import os
from pathlib import Path
from typing import List, Dict, Any

from langchain.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from app.core.config import settings


async def process_document(document_id: int, file_path: str) -> str:
    """
    Process a document for RAG.

    Args:
        document_id: The ID of the document in the database.
        file_path: The path to the document file.

    Returns:
        The path to the vector store.
    """
    # Create directory for vector stores if it doesn't exist
    vector_stores_dir = Path("vector_stores")
    vector_stores_dir.mkdir(exist_ok=True)

    # Create directory for this document's vector store
    vector_store_path = vector_stores_dir / f"document_{document_id}"
    vector_store_path.mkdir(exist_ok=True)

    # Load document based on file type
    file_extension = Path(file_path).suffix.lower()

    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension == ".csv":
        loader = CSVLoader(file_path)
    else:
        # Default to text loader for other file types
        loader = TextLoader(file_path)

    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(documents)

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Save vector store
    vector_store.save_local(str(vector_store_path))

    return str(vector_store_path)


async def query_document(vector_store_path: str, query: str) -> str:
    """
    Query a document using RAG.

    Args:
        vector_store_path: The path to the vector store.
        query: The query to run against the document.

    Returns:
        The response from the RAG pipeline.
    """
    # Load vector store
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    vector_store = FAISS.load_local(
        vector_store_path, embeddings, allow_dangerous_deserialization=True
    )

    # Create retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )

    # Create QA chain
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY,
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    # Run query
    result = qa_chain({"query": query})

    return result["result"]
