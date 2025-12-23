from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import logging
from app.models.schemas import IngestRequest, IngestResponse
from app.services.rag_service import rag_service
from app.utils.config import Config

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(request: IngestRequest):
    """
    Endpoint to ingest document content into the RAG system
    """
    try:
        # Validate configuration
        Config.validate()

        # Process the ingestion request using RAG service
        document_id = await rag_service.ingest_document(
            content=request.content,
            title=request.document_title,
            url=request.document_url,
            metadata=request.metadata
        )

        return IngestResponse(
            message="Document successfully ingested",
            document_id=document_id,
            chunks_count=len(request.content) // Config.CHUNK_SIZE + 1  # Approximate count
        )
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest-file")
async def ingest_file_endpoint(file: UploadFile = File(...), title: str = Form(...), url: str = Form(None)):
    """
    Endpoint to upload and ingest a document file
    """
    try:
        # Validate configuration
        Config.validate()

        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')

        # Process the ingestion
        document_id = await rag_service.ingest_document(
            content=content_str,
            title=title,
            url=url
        )

        return IngestResponse(
            message=f"File {file.filename} successfully ingested",
            document_id=document_id,
            chunks_count=len(content_str) // Config.CHUNK_SIZE + 1  # Approximate count
        )
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except UnicodeDecodeError:
        logger.error("File encoding error: unable to decode file as UTF-8")
        raise HTTPException(status_code=400, detail="File must be encoded as UTF-8")
    except Exception as e:
        logger.error(f"Error in ingest file endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))