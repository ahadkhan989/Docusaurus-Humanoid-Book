# rag-ingest.py
# This script is a conceptual implementation of the vector ingestion pipeline.

import os
from langchain.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
DOCS_PATH = "../docs"  # Path to the Docusaurus docs directory
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "ai_native_textbook"

def ingest_documents():
    """
    Chunks Markdown documents, creates embeddings, and stores them in Qdrant.
    """
    print("Starting document ingestion...")

    # 1. Load Markdown documents from the Docusaurus `docs` directory
    print(f"Loading documents from: {DOCS_PATH}")
    loader = DirectoryLoader(
        DOCS_PATH,
        glob="**/*.md",
        loader_cls=UnstructuredMarkdownLoader,
        show_progress=True,
        use_multithreading=True,
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    # 2. Split documents into smaller chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    # 3. Create embeddings for the chunks
    print("Creating embeddings...")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # 4. Store the chunks and their embeddings in Qdrant
    print("Storing chunks and embeddings in Qdrant...")
    Qdrant.from_documents(
        chunks,
        embeddings,
        url=QDRANT_URL,
        prefer_grpc=True,
        api_key=QDRANT_API_KEY,
        collection_name=COLLECTION_NAME,
    )
    print("Ingestion complete!")


if __name__ == "__main__":
    # This script would be run as a standalone process to populate the vector store.
    # Ensure you have a .env file in the same directory with:
    # QDRANT_URL="your_qdrant_url"
    # QDRANT_API_KEY="your_qdrant_api_key"
    # OPENAI_API_KEY="your_openai_api_key"
    
    # For this conceptual implementation, we will just print a success message.
    print("Conceptual RAG Ingestion Pipeline")
    print("This script would perform the following steps:")
    print("1. Load Markdown documents from the Docusaurus `docs` directory.")
    print("2. Split documents into smaller chunks.")
    print("3. Create embeddings for the chunks using OpenAI.")
    print("4. Store the chunks and their embeddings in a Qdrant vector store.")
    
    # ingest_documents() # This would be called in a real implementation
