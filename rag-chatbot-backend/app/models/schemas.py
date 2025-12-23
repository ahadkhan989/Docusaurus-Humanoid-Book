from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request model for general chat endpoint
    """
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    top_k: Optional[int] = 5  # Number of chunks to retrieve from vector store


class ChatSelectionRequest(BaseModel):
    """
    Request model for chat about user-selected text
    """
    selected_text: str
    question: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    top_k: Optional[int] = 5


class ChatResponse(BaseModel):
    """
    Response model for chat endpoints
    """
    response: str
    sources: List[str]
    conversation_id: str
    timestamp: datetime


class IngestRequest(BaseModel):
    """
    Request model for document ingestion
    """
    content: str
    document_title: str
    document_url: Optional[str] = None
    metadata: Optional[dict] = {}


class IngestResponse(BaseModel):
    """
    Response model for document ingestion
    """
    message: str
    document_id: str
    chunks_count: int


class Source(BaseModel):
    """
    Model for source information
    """
    id: str
    content: str
    score: float
    metadata: dict


class SourcesResponse(BaseModel):
    """
    Response model for sources endpoint
    """
    sources: List[Source]