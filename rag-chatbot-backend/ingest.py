# --------->  Sub se pehli file code <----------

# """
# Content ingestion script to load markdown files from Docusaurus
# and populate the Qdrant vector database
# """

# import os
# import sys
# import glob
# import json
# from pathlib import Path
# from typing import List, Dict
# import re

# import requests
# from dotenv import load_dotenv
# import openai
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams, PointStruct

# load_dotenv()

# # Configuration
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# QDRANT_URL = os.getenv("QDRANT_URL")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# DOCS_PATH = "../docs"  # Path to Docusaurus docs folder
# COLLECTION_NAME = "docusaurus_content"
# CHUNK_SIZE = 500  # Characters per chunk
# CHUNK_OVERLAP = 100

# openai.api_key = OPENAI_API_KEY

# class ContentIngestionManager:
#     def __init__(self):
#         self.qdrant_client = QdrantClient(
#             url=QDRANT_URL,
#             api_key=QDRANT_API_KEY
#         )
#         self.collection_name = COLLECTION_NAME
        
#     def read_markdown_files(self) -> List[Dict[str, str]]:
#         """Read all markdown files from docs folder"""
#         documents = []
        
#         # Find all .md and .mdx files
#         md_files = glob.glob(os.path.join(DOCS_PATH, "**/*.md*"), recursive=True)
#         md_files += glob.glob(os.path.join(DOCS_PATH, "**/*.mdx"), recursive=True)
        
#         print(f"Found {len(md_files)} markdown files")
        
#         for file_path in md_files:
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read()
                
#                 # Extract title from frontmatter or filename
#                 title = self.extract_title(content, file_path)
                
#                 # Remove frontmatter
#                 content = self.remove_frontmatter(content)
                
#                 documents.append({
#                     'path': file_path,
#                     'title': title,
#                     'content': content
#                 })
#                 print(f"✓ Loaded: {file_path}")
                
#             except Exception as e:
#                 print(f"✗ Error reading {file_path}: {str(e)}")
        
#         return documents
    
#     def extract_title(self, content: str, file_path: str) -> str:
#         """Extract title from frontmatter or use filename"""
#         # Try to get from frontmatter
#         title_match = re.search(r'title:\s*["\']?([^"\'\n]+)', content)
#         if title_match:
#             return title_match.group(1).strip()
        
#         # Fallback to filename
#         filename = os.path.basename(file_path)
#         return filename.replace('.md', '').replace('.mdx', '').replace('-', ' ').title()
    
#     def remove_frontmatter(self, content: str) -> str:
#         """Remove YAML/TOML frontmatter from markdown"""
#         if content.startswith('---'):
#             parts = content.split('---', 2)
#             if len(parts) >= 3:
#                 return parts[2].strip()
#         return content
    
#     def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, 
#                    overlap: int = CHUNK_OVERLAP) -> List[str]:
#         """Split text into overlapping chunks"""
#         chunks = []
#         start = 0
        
#         while start < len(text):
#             end = start + chunk_size
#             chunk = text[start:end]
#             chunks.append(chunk)
#             start = end - overlap
        
#         return chunks
    
#     def get_embeddings(self, text: str) -> List[float]:
#         """Get embeddings from OpenAI"""
#         response = openai.Embedding.create(
#             input=text,
#             model="text-embedding-3-small"
#         )
#         return response['data'][0]['embedding']
    
#     def create_collection(self):
#         """Create Qdrant collection if it doesn't exist"""
#         try:
#             self.qdrant_client.get_collection(self.collection_name)
#             print(f"Collection '{self.collection_name}' already exists")
#         except:
#             print(f"Creating collection '{self.collection_name}'...")
#             self.qdrant_client.create_collection(
#                 collection_name=self.collection_name,
#                 vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
#             )
#             print("✓ Collection created")
    
#     def ingest_documents(self, documents: List[Dict[str, str]]):
#         """Ingest documents into Qdrant"""
#         self.create_collection()
        
#         point_id = 0
#         total_points = 0
        
#         for doc in documents:
#             print(f"\nProcessing: {doc['title']}")
            
#             # Chunk the content
#             chunks = self.chunk_text(doc['content'])
#             print(f"  Created {len(chunks)} chunks")
            
#             for i, chunk in enumerate(chunks):
#                 try:
#                     # Get embedding
#                     embedding = self.get_embeddings(chunk)
                    
#                     # Create point
#                     point = PointStruct(
#                         id=point_id,
#                         vector=embedding,
#                         payload={
#                             'text': chunk,
#                             'title': doc['title'],
#                             'source': doc['path'],
#                             'chunk_index': i,
#                             'document_title': doc['title']
#                         }
#                     )
                    
#                     # Upsert to Qdrant
#                     self.qdrant_client.upsert(
#                         collection_name=self.collection_name,
#                         points=[point]
#                     )
                    
#                     point_id += 1
#                     total_points += 1
                    
#                     if (i + 1) % 5 == 0:
#                         print(f"  ✓ Processed {i + 1}/{len(chunks)} chunks")
                    
#                 except Exception as e:
#                     print(f"  ✗ Error processing chunk {i}: {str(e)}")
        
#         print(f"\n✓ Ingestion complete! Total points: {total_points}")
#         return total_points
    
#     def get_collection_stats(self):
#         """Get collection statistics"""
#         collection_info = self.qdrant_client.get_collection(self.collection_name)
#         print(f"\nCollection Stats:")
#         print(f"  Points count: {collection_info.points_count}")
#         print(f"  Vector size: {collection_info.config.params.vectors.size}")

# def main():
#     print("=" * 50)
#     print("Docusaurus Content Ingestion Manager")
#     print("=" * 50)
    
#     manager = ContentIngestionManager()
    
#     # Read markdown files
#     print("\n[1/3] Reading markdown files...")
#     documents = manager.read_markdown_files()
    
#     if not documents:
#         print("✗ No markdown files found!")
#         return
    
#     print(f"✓ Found {len(documents)} documents")
    
#     # Ingest documents
#     print("\n[2/3] Ingesting documents...")
#     manager.ingest_documents(documents)
    
#     # Get stats
#     print("\n[3/3] Collection statistics...")
#     manager.get_collection_stats()
    
#     print("\n" + "=" * 50)
#     print("✓ Content ingestion successful!")
#     print("=" * 50)

# if __name__ == "__main__":
#     main()


"""
Content ingestion script to load markdown files from Docusaurus
and populate the Qdrant vector database
"""

import os
import sys
import glob
import json
import re
import time
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
DOCS_PATH = "../docs"  # Path to Docusaurus docs folder
COLLECTION_NAME = "docusaurus_content"
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 100

# Validate API keys
if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not set in .env")
    sys.exit(1)

if not QDRANT_URL or not QDRANT_API_KEY:
    print("❌ ERROR: QDRANT_URL or QDRANT_API_KEY not set in .env")
    sys.exit(1)

print("✓ OpenAI API Key loaded")
print(f"✓ Qdrant URL: {QDRANT_URL}")
print(f"✓ Qdrant API Key: {'*' * 10}...{QDRANT_API_KEY[-5:]}")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)


class ContentIngestionManager:
    def __init__(self):
        try:
            # Qdrant client connect karo with proper authentication
            self.qdrant_client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
                timeout=30.0
            )
            # Connection test karo
            self.qdrant_client.get_collections()
            print("✓ Connected to Qdrant Cloud successfully!")
        except Exception as e:
            print(f"❌ Failed to connect to Qdrant: {str(e)}")
            print("\nYadgar rakhne ke liye:")
            print("1. Qdrant Cloud URL aur API Key check karo: https://cloud.qdrant.io/")
            print("2. .env file me sahi values set karo")
            print("3. API Key me spaces nahi honi chahiye")
            sys.exit(1)
        
        self.collection_name = COLLECTION_NAME
        
    def read_markdown_files(self) -> List[Dict[str, str]]:
        """Read all markdown files from docs folder"""
        documents = []
        
        # Find all .md and .mdx files
        md_files = glob.glob(os.path.join(DOCS_PATH, "**/*.md*"), recursive=True)
        # Remove duplicates (agar same file .md aur .mdx dono ho)
        md_files = list(set(md_files))
        md_files.sort()
        
        print(f"Found {len(md_files)} markdown files")
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract title from frontmatter or filename
                title = self.extract_title(content, file_path)
                
                # Remove frontmatter
                content = self.remove_frontmatter(content)
                
                if content.strip():  # Only add non-empty documents
                    documents.append({
                        'path': file_path,
                        'title': title,
                        'content': content
                    })
                    print(f"✓ Loaded: {file_path}")
                
            except Exception as e:
                print(f"✗ Error reading {file_path}: {str(e)}")
        
        return documents
    
    def extract_title(self, content: str, file_path: str) -> str:
        """Extract title from frontmatter or use filename"""
        # Try to get from frontmatter
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)', content)
        if title_match:
            return title_match.group(1).strip()
        
        # Fallback to filename
        filename = os.path.basename(file_path)
        return filename.replace('.md', '').replace('.mdx', '').replace('-', ' ').title()
    
    def remove_frontmatter(self, content: str) -> str:
        """Remove YAML/TOML frontmatter from markdown"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return content
    
    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, 
                   overlap: int = CHUNK_OVERLAP) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
            start = end - overlap
        
        return chunks if chunks else [""]
    
    def get_embeddings(self, text: str) -> List[float]:
        """Get embeddings from OpenAI"""
        try:
            response = openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Embedding error: {str(e)}")
            raise
    
    def create_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            collections = self.qdrant_client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name in collection_names:
                print(f"✓ Collection '{self.collection_name}' already exists")
            else:
                print(f"Creating collection '{self.collection_name}'...")
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
                print("✓ Collection created successfully")
        except Exception as e:
            print(f"❌ Collection creation error: {str(e)}")
            raise
    
    def ingest_documents(self, documents: List[Dict[str, str]]):
        """Ingest documents into Qdrant"""
        self.create_collection()
        
        point_id = 0
        total_points = 0
        
        for doc_idx, doc in enumerate(documents, 1):
            print(f"\n[{doc_idx}/{len(documents)}] Processing: {doc['title']}")
            
            # Chunk the content
            chunks = self.chunk_text(doc['content'])
            print(f"  Created {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                try:
                    # Get embedding
                    embedding = self.get_embeddings(chunk)
                    
                    # Create point
                    point = PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            'text': chunk[:1000],  # Store first 1000 chars in payload
                            'title': doc['title'],
                            'source': doc['path'],
                            'chunk_index': i,
                            'document_title': doc['title']
                        }
                    )
                    
                    # Upsert to Qdrant
                    self.qdrant_client.upsert(
                        collection_name=self.collection_name,
                        points=[point]
                    )
                    
                    point_id += 1
                    total_points += 1
                    
                    if (i + 1) % 5 == 0:
                        print(f"  ✓ Processed {i + 1}/{len(chunks)} chunks")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"  ✗ Error processing chunk {i}: {str(e)}")
        
        print(f"\n✓ Ingestion complete! Total points: {total_points}")
        return total_points
    
    def get_collection_stats(self):
        """Get collection statistics"""
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            print(f"\nCollection Statistics:")
            print(f"  Points count: {collection_info.points_count}")
            print(f"  Vector size: {collection_info.config.params.vectors.size}")
        except Exception as e:
            print(f"Error getting stats: {str(e)}")


def main():
    print("=" * 60)
    print("Docusaurus Content Ingestion Manager")
    print("=" * 60)
    
    manager = ContentIngestionManager()
    
    # Read markdown files
    print("\n[1/3] Reading markdown files...")
    documents = manager.read_markdown_files()
    
    if not documents:
        print("✗ No markdown files found!")
        print(f"Check if '../docs' path exists: {os.path.abspath(DOCS_PATH)}")
        return
    
    print(f"✓ Found {len(documents)} documents\n")
    
    # Ingest documents
    print("[2/3] Ingesting documents into Qdrant...")
    manager.ingest_documents(documents)
    
    # Get stats
    print("\n[3/3] Collection statistics...")
    manager.get_collection_stats()
    
    print("\n" + "=" * 60)
    print("✓ Content ingestion successful!")
    print("=" * 60)


if __name__ == "__main__":
    main()