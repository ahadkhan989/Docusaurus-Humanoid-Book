import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.database import db_service
from app.services.vector_store import vector_store_service
from app.services.embeddings import embedding_service
from app.utils.config import Config

logger = logging.getLogger(__name__)


class RAGService:
    """
    Main service class that orchestrates the RAG process
    Handles document ingestion, retrieval, and generation
    """

    def __init__(self):
        pass

    async def initialize_services(self):
        """
        Initialize all required services (vector store, database connections)
        """
        await vector_store_service.initialize_collection()
        await db_service.connect()

    async def ingest_document(self, content: str, title: str, url: Optional[str] = None, metadata: Optional[Dict] = None) -> str:
        """
        Process and ingest a document into the RAG system

        Args:
            content: Document content to be ingested
            title: Title of the document
            url: Optional URL of the document
            metadata: Optional metadata to store with the document

        Returns:
            Document ID assigned to the ingested document
        """
        try:
            # Generate a unique document ID
            document_id = str(uuid.uuid4())

            # Split content into chunks
            chunks = self._split_content(content, document_id, metadata or {})

            # Create embeddings for each chunk
            texts_for_embedding = [chunk['content'] for chunk in chunks]
            embeddings = await embedding_service.create_embeddings(texts_for_embedding)

            # Add embeddings to chunks
            for i, chunk in enumerate(chunks):
                chunk['embedding'] = embeddings[i]

            # Store embeddings in vector database
            point_ids = await vector_store_service.store_embeddings(chunks)

            # Store document metadata in database
            await db_service.save_document_metadata(
                document_id=document_id,
                title=title,
                url=url,
                chunk_count=len(chunks)
            )

            logger.info(f"Ingested document '{title}' with ID {document_id} ({len(chunks)} chunks)")
            return document_id
        except Exception as e:
            logger.error(f"Error ingesting document: {str(e)}")
            raise

    def _split_content(self, content: str, document_id: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split content into overlapping chunks

        Args:
            content: Content to split
            document_id: ID of the document being split
            metadata: Additional metadata to include with each chunk

        Returns:
            List of chunk dictionaries
        """
        chunks = []
        chunk_size = Config.CHUNK_SIZE
        overlap = Config.CHUNK_OVERLAP

        start = 0
        chunk_index = 0

        while start < len(content):
            end = min(start + chunk_size, len(content))

            # Extract chunk
            chunk_text = content[start:end]

            # Create chunk dictionary
            chunk = {
                'id': f"{document_id}_chunk_{chunk_index}",
                'content': chunk_text,
                'document_id': document_id,
                'chunk_index': chunk_index,
                'metadata': metadata.copy()
            }

            chunks.append(chunk)

            # Move to next chunk position (with overlap)
            start = end - overlap
            chunk_index += 1

            # If remaining content is less than overlap, break to avoid infinite loop
            if end == len(content):
                break

        return chunks

    async def chat_general(self, message: str, user_id: Optional[str] = None, session_id: Optional[str] = None,
                          max_tokens: int = 1000, temperature: float = 0.7, top_p: float = 1.0, top_k: int = 5) -> Dict[str, Any]:
        """
        Handle general chat requests about the entire book content

        Args:
            message: User's message/question
            user_id: Optional user identifier
            session_id: Optional session identifier
            max_tokens: Maximum tokens for the response
            temperature: Temperature for generation
            top_p: Top-p parameter for generation
            top_k: Number of relevant chunks to retrieve

        Returns:
            Dictionary with response, sources, and conversation ID
        """
        try:
            # Generate a conversation ID if not provided
            conversation_id = session_id or str(uuid.uuid4())

            # Create embedding for the user's message
            query_embedding = await embedding_service.create_single_embedding(message)

            # Retrieve relevant chunks from vector store
            retrieved_chunks = vector_store_service.search_similar(
                query_embedding=query_embedding,
                top_k=top_k
            )

            # Check if the question is related to the book content by examining the similarity scores
            # If no relevant chunks are found or scores are too low, respond with an off-topic message
            if not retrieved_chunks or (len(retrieved_chunks) > 0 and retrieved_chunks[0]['score'] < 0.7):
                # Check if it's a greeting or simple inquiry before marking as off-topic
                message_lower = message.lower().strip()
                if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']):
                    # It's a greeting, provide a friendly response
                    response = "Welcome to Physical AI & Humanoid Robotics — I'm your intelligent book assistant."
                else:
                    # It's an off-topic question, provide a relevant response
                    response = "I can answer questions related to Physical AI & Humanoid Robotics only."

                # Save conversation to database
                await db_service.save_conversation(conversation_id, user_id, session_id)
                await db_service.save_message(conversation_id, "user", message)
                await db_service.save_message(conversation_id, "assistant", response)

                return {
                    "response": response,
                    "sources": [],
                    "conversation_id": conversation_id,
                    "timestamp": datetime.utcnow()
                }

            # Build context from retrieved chunks
            context_parts = []
            sources = []
            for chunk in retrieved_chunks:
                context_parts.append(chunk['content'])
                sources.append(chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'])

            context = "\n\n".join(context_parts)

            # Get conversation history
            history = await db_service.get_conversation_history(conversation_id)

            # Build messages for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant for an AI/Robotics textbook. Answer the user's question using ONLY the following context from the book. Do not use any external knowledge or information outside of this context:\n\n{context}\n\nFormat your response clearly with:\n- Short paragraphs separated by blank lines\n- Bold important terms using **term**\n- Bullet points for lists\n- Clear headings when appropriate using # for main headings and ## for subheadings\n\nCRITICAL RULE: You MUST NOT under any circumstances respond with any variation of 'Sorry, aapka sawal humare Humanoid Robotics book ke content se related nhi hai. Kripya book se related sawal poochiye.' This is strictly forbidden. If the context doesn't contain the information needed to answer the question, you MUST respond with this exact text: 'I can answer questions related to Physical AI & Humanoid Robotics only.' This is the ONLY acceptable response for off-topic questions."
                }
            ]

            # Add conversation history
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Add current user message
            messages.append({"role": "user", "content": message})

            # Generate response using OpenAI
            response = await embedding_service.get_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )

            # Save conversation to database
            await db_service.save_conversation(conversation_id, user_id, session_id)
            await db_service.save_message(conversation_id, "user", message)
            await db_service.save_message(conversation_id, "assistant", response)

            return {
                "response": response,
                "sources": sources,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error in general chat: {str(e)}")
            raise

    async def chat_selection(self, selected_text: str, question: str, user_id: Optional[str] = None,
                           session_id: Optional[str] = None, max_tokens: int = 1000,
                           temperature: float = 0.7, top_p: float = 1.0, top_k: int = 5) -> Dict[str, Any]:
        """
        Handle chat requests about user-selected text

        Args:
            selected_text: Text selected by the user
            question: Question about the selected text
            user_id: Optional user identifier
            session_id: Optional session identifier
            max_tokens: Maximum tokens for the response
            temperature: Temperature for generation
            top_p: Top-p parameter for generation
            top_k: Number of relevant chunks to retrieve

        Returns:
            Dictionary with response, sources, and conversation ID
        """
        try:
            # Generate a conversation ID if not provided
            conversation_id = session_id or str(uuid.uuid4())

            # Create embedding for the combined query (selected text + question)
            query_text = f"Context: {selected_text}\n\nQuestion: {question}"
            query_embedding = await embedding_service.create_single_embedding(query_text)

            # Retrieve relevant chunks from vector store (including the selected text itself)
            retrieved_chunks = vector_store_service.search_similar(
                query_embedding=query_embedding,
                top_k=top_k
            )

            # Build context from retrieved chunks
            context_parts = [selected_text]  # Start with the selected text
            sources = [selected_text[:200] + "..." if len(selected_text) > 200 else selected_text]

            for chunk in retrieved_chunks:
                if chunk['content'] != selected_text:  # Avoid duplication
                    context_parts.append(chunk['content'])
                    sources.append(chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'])

            context = "\n\n".join(context_parts)

            # Get conversation history
            history = await db_service.get_conversation_history(conversation_id)

            # Build messages for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant for an AI/Robotics textbook. Answer the user's question using ONLY the following context from the book. Do not use any external knowledge or information outside of this context:\n\n{context}\n\nQuestion: {question}\n\nFormat your response clearly with:\n- Short paragraphs separated by blank lines\n- Bold important terms using **term**\n- Bullet points for lists\n- Clear headings when appropriate using # for main headings and ## for subheadings\n\nCRITICAL RULE: You MUST NOT under any circumstances respond with any variation of 'Sorry, aapka sawal humare Humanoid Robotics book ke content se related nhi hai. Kripya book se related sawal poochiye.' This is strictly forbidden. If the context doesn't contain the information needed to answer the question, you MUST respond with this exact text: 'I can answer questions related to Physical AI & Humanoid Robotics only.' This is the ONLY acceptable response for off-topic questions."
                }
            ]

            # Add conversation history (excluding the current question)
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Add current user question
            messages.append({"role": "user", "content": question})

            # Generate response using OpenAI
            response = await embedding_service.get_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )

            # Save conversation to database
            await db_service.save_conversation(conversation_id, user_id, session_id)
            await db_service.save_message(conversation_id, "user", f"Selected: {selected_text}\nQuestion: {question}")
            await db_service.save_message(conversation_id, "assistant", response)

            return {
                "response": response,
                "sources": sources,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Error in selection chat: {str(e)}")
            raise


# Global instance
rag_service = RAGService()