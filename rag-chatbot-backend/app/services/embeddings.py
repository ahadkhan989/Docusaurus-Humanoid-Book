import logging
import asyncio
from typing import List, Dict, Any
from openai import AsyncOpenAI
from app.utils.config import Config

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service class for generating embeddings using OpenAI API
    """

    def __init__(self):
        self._client = None
        self.model = Config.OPENAI_EMBEDDING_MODEL

    @property
    def client(self):
        if self._client is None:
            self._client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
        return self._client

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI API

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        try:
            # Batch embeddings for efficiency (OpenAI supports up to 2048 texts per request)
            # But we'll use a conservative batch size to avoid rate limits
            batch_size = 20
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]

                response = await self.client.embeddings.create(
                    input=batch_texts,
                    model=self.model
                )

                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)

            logger.info(f"Generated embeddings for {len(texts)} text chunks")
            return all_embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    async def create_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Text to generate embedding for

        Returns:
            Embedding vector (list of floats)
        """
        try:
            response = await self.client.embeddings.create(
                input=[text],
                model=self.model
            )

            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding for text of length {len(text)}")
            return embedding
        except Exception as e:
            logger.error(f"Error generating single embedding: {str(e)}")
            raise

    async def get_chat_completion(self, messages: List[Dict[str, str]],
                                 max_tokens: int = 1000,
                                 temperature: float = 0.7,
                                 top_p: float = 1.0) -> str:
        """
        Generate chat completion using OpenAI API

        Args:
            messages: List of messages in the conversation (with role and content)
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter

        Returns:
            Generated response text
        """
        try:
            response = await self.client.chat.completions.create(
                model=Config.OPENAI_CHAT_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )

            result = response.choices[0].message.content.strip()
            logger.info(f"Generated chat completion with {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Error generating chat completion: {str(e)}")
            raise


# Global instance
embedding_service = EmbeddingService()