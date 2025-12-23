import asyncpg
import logging
from typing import List, Dict, Any, Optional
from app.utils.config import Config

logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Service class for PostgreSQL database operations
    Handles chat history, document metadata, and user sessions
    """

    def __init__(self):
        self.pool = None
        self._initialized = False

    async def connect(self):
        """
        Establish connection pool to PostgreSQL database
        """
        try:
            self.pool = await asyncpg.create_pool(Config.DATABASE_URL)
            logger.info("Connected to PostgreSQL database")

            # Initialize tables if they don't exist
            await self._initialize_tables()
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise

    async def _initialize_tables(self):
        """
        Create necessary tables if they don't exist
        """
        async with self.pool.acquire() as conn:
            # Create documents table for metadata
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    document_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT,
                    content_hash TEXT,
                    chunk_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create document_chunks table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id SERIAL PRIMARY KEY,
                    document_id TEXT,
                    chunk_index INTEGER,
                    content TEXT NOT NULL,
                    embedding_id TEXT,  -- Reference to Qdrant point ID
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create conversations table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    conversation_id TEXT UNIQUE NOT NULL,
                    user_id TEXT,
                    session_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create messages table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id TEXT REFERENCES conversations(conversation_id),
                    role TEXT NOT NULL,  -- 'user' or 'assistant'
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            logger.info("Database tables initialized")

    async def save_document_metadata(self, document_id: str, title: str, url: Optional[str], chunk_count: int) -> bool:
        """
        Save document metadata to database
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO documents (document_id, title, url, chunk_count)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (document_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        url = EXCLUDED.url,
                        chunk_count = EXCLUDED.chunk_count,
                        updated_at = CURRENT_TIMESTAMP
                """, document_id, title, url, chunk_count)

                logger.info(f"Saved document metadata for {document_id}")
                return True
        except Exception as e:
            logger.error(f"Error saving document metadata: {str(e)}")
            return False

    async def save_conversation(self, conversation_id: str, user_id: Optional[str] = None, session_id: Optional[str] = None) -> bool:
        """
        Create or update a conversation record
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO conversations (conversation_id, user_id, session_id)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (conversation_id) DO UPDATE SET
                        user_id = EXCLUDED.user_id,
                        session_id = EXCLUDED.session_id,
                        updated_at = CURRENT_TIMESTAMP
                """, conversation_id, user_id, session_id)

                logger.info(f"Conversation saved: {conversation_id}")
                return True
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            return False

    async def save_message(self, conversation_id: str, role: str, content: str) -> bool:
        """
        Save a message to the conversation history
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO messages (conversation_id, role, content)
                    VALUES ($1, $2, $3)
                """, conversation_id, role, content)

                logger.info(f"Message saved to conversation: {conversation_id}")
                return True
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
            return False

    async def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history for a specific conversation
        """
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT role, content, timestamp
                    FROM messages
                    WHERE conversation_id = $1
                    ORDER BY timestamp ASC
                """, conversation_id)

                return [{"role": row["role"], "content": row["content"], "timestamp": row["timestamp"]} for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {str(e)}")
            return []

    async def close(self):
        """
        Close the database connection pool
        """
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")


# Global instance
db_service = DatabaseService()