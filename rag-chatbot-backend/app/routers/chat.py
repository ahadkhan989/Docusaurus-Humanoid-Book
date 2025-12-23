from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import List
from datetime import datetime
from app.models.schemas import ChatRequest, ChatSelectionRequest, ChatResponse, SourcesResponse
from app.services.rag_service import rag_service
from app.utils.config import Config

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    General chat endpoint for questions about the entire book content
    """
    try:
        # Validate configuration
        Config.validate()

        # Process the chat request using RAG service
        result = await rag_service.chat_general(
            message=request.message,
            user_id=request.user_id,
            session_id=request.session_id,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k
        )

        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            conversation_id=result["conversation_id"],
            timestamp=result["timestamp"]
        )
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Additional compatibility endpoint for the frontend format
@router.post("/chat/compat")
async def chat_compatibility_endpoint(
    query: str,
    session_id: str = "anonymous",
    conversation_history: List[dict] = None
):
    """
    Compatibility endpoint for the frontend format
    Expects query, session_id, and conversation_history from frontend
    Returns response in the format the frontend expects (answer and sources)
    """
    try:
        # Validate configuration
        Config.validate()

        # Process the chat request using RAG service
        result = await rag_service.chat_general(
            message=query,
            user_id="anonymous",
            session_id=session_id,
            max_tokens=1000,
            temperature=0.7,
            top_p=1.0,
            top_k=5
        )

        return {
            "answer": result["response"],
            "sources": result["sources"]
        }
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error in chat compatibility endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Compatibility endpoint that accepts JSON body
@router.post("/chat/json-compat")
async def chat_json_compatibility_endpoint(request: dict):
    """
    JSON compatibility endpoint for the frontend format
    Accepts JSON body with query, session_id, and conversation_history
    Returns response in the format the frontend expects (answer and sources)
    """
    try:
        # Validate configuration
        Config.validate()

        query = request.get("query", "")
        session_id = request.get("session_id", "anonymous")
        conversation_history = request.get("conversation_history", [])

        # Process the chat request using RAG service
        result = await rag_service.chat_general(
            message=query,
            user_id="anonymous",
            session_id=session_id,
            max_tokens=1000,
            temperature=0.7,
            top_p=1.0,
            top_k=5
        )

        return {
            "answer": result["response"],
            "sources": result["sources"]
        }
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error in chat JSON compatibility endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat-selection", response_model=ChatResponse)
async def chat_selection_endpoint(request: ChatSelectionRequest):
    """
    Chat endpoint for questions about user-selected text
    """
    try:
        # Validate configuration
        Config.validate()

        # Process the chat selection request using RAG service
        result = await rag_service.chat_selection(
            selected_text=request.selected_text,
            question=request.question,
            user_id=request.user_id,
            session_id=request.session_id,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k
        )

        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            conversation_id=result["conversation_id"],
            timestamp=result["timestamp"]
        )
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error in chat selection endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/compatibility")
async def chat_compatibility_endpoint(
    query: str,
    session_id: str = "anonymous",
    conversation_history: List[dict] = []
):
    """
    Compatibility endpoint for the frontend format
    Frontend sends query, session_id, and conversation_history
    """
    try:
        # Validate configuration
        Config.validate()

        # Convert frontend format to backend format
        chat_request = ChatRequest(
            message=query,
            session_id=session_id,
            user_id="anonymous"  # Default user_id
        )

        # Process the chat request using RAG service
        result = await rag_service.chat_general(
            message=chat_request.message,
            user_id=chat_request.user_id,
            session_id=chat_request.session_id,
            max_tokens=chat_request.max_tokens,
            temperature=chat_request.temperature,
            top_p=chat_request.top_p,
            top_k=chat_request.top_k
        )

        return {
            "answer": result["response"],
            "sources": result["sources"]
        }
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error in chat compatibility endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sources", response_model=SourcesResponse)
async def get_sources_endpoint(conversation_id: str):
    """
    Return sources used for answers in a specific conversation
    """
    try:
        # This would typically retrieve sources from the database
        # For now, we'll return an empty list as sources are already returned in the chat response
        # In a real implementation, you might want to store sources separately in the DB
        return SourcesResponse(sources=[])
    except Exception as e:
        logger.error(f"Error in sources endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))