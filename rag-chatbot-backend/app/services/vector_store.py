import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.utils.config import Config

logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Service class for Qdrant vector database operations
    Handles document embeddings storage and retrieval
    """

    def __init__(self):
        self._client = None
        self.collection_name = Config.QDRANT_COLLECTION_NAME

    @property
    def client(self):
        if self._client is None:
            self._client = QdrantClient(
                url=Config.QDRANT_URL,
                api_key=Config.QDRANT_API_KEY,
                prefer_grpc=True
            )
        return self._client

    async def initialize_collection(self):
        """
        Initialize the collection in Qdrant with appropriate vector configuration
        """
        try:
            # Check if collection exists
            # Note: get_collections() may not be async in newer versions
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate vector size for OpenAI embeddings (1536 dimensions)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # OpenAI ada-002 embedding dimension
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection '{self.collection_name}' in Qdrant")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists in Qdrant")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise

    async def store_embeddings(self, chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Store document chunks with their embeddings in Qdrant

        Args:
            chunks: List of dictionaries containing 'id', 'content', 'metadata'

        Returns:
            List of Qdrant point IDs for the stored chunks
        """
        try:
            points = []
            for chunk in chunks:
                point = models.PointStruct(
                    id=chunk['id'],
                    vector=chunk['embedding'],
                    payload={
                        "content": chunk['content'],
                        "document_id": chunk['document_id'],
                        "chunk_index": chunk.get('chunk_index', 0),
                        **chunk.get('metadata', {})
                    }
                )
                points.append(point)

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Stored {len(points)} embeddings in Qdrant")
            return [point.id for point in points]
        except Exception as e:
            logger.error(f"Error storing embeddings in Qdrant: {str(e)}")
            raise

    def search_similar(self, query_embedding: List[float], top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents based on embedding similarity

        Args:
            query_embedding: The embedding vector to search for
            top_k: Number of similar documents to return
            filters: Optional filters to apply to the search

        Returns:
            List of similar documents with scores
        """
        try:
            # Prepare filters if provided
            search_filter = None
            if filters:
                must_conditions = []
                for key, value in filters.items():
                    must_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )

                if must_conditions:
                    search_filter = models.Filter(must=must_conditions)

            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter,
                with_payload=True
            )

            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "score": hit.score,
                    "metadata": {k: v for k, v in hit.payload.items() if k != "content"}
                })

            logger.info(f"Found {len(results)} similar documents in Qdrant")
            return results
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {str(e)}")
            raise

    async def delete_document(self, document_id: str):
        """
        Delete all chunks associated with a document ID
        """
        try:
            # Find all points with the given document_id
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id)
                        )
                    ]
                ),
                limit=10000  # Assuming reasonable max number of chunks per document
            )

            # Extract point IDs
            point_ids = [point.id for point in scroll_result.points]

            if point_ids:
                # Delete points
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(
                        points=point_ids
                    )
                )
                logger.info(f"Deleted {len(point_ids)} chunks for document {document_id} from Qdrant")
            else:
                logger.warning(f"No chunks found for document {document_id} in Qdrant")
        except Exception as e:
            logger.error(f"Error deleting document from Qdrant: {str(e)}")
            raise

    async def get_point_by_id(self, point_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single point by its ID
        """
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[point_id],
                with_payload=True,
                with_vectors=False
            )

            if points:
                point = points[0]
                return {
                    "id": point.id,
                    "content": point.payload.get("content", ""),
                    "metadata": {k: v for k, v in point.payload.items() if k != "content"}
                }
            return None
        except Exception as e:
            logger.error(f"Error retrieving point from Qdrant: {str(e)}")
            return None


# Global instance
vector_store_service = VectorStoreService()