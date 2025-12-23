from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
from .routers import chat, ingest
from .services.rag_service import rag_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot Backend",
    description="A Retrieval-Augmented Generation chatbot backend for Docusaurus-based AI/Robotics textbook",
    version="1.0.0"
)

# Add CORS middleware to allow requests from Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(ingest.router, prefix="/api", tags=["ingest"])

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify the backend is running
    """
    return {"status": "healthy", "message": "RAG Chatbot Backend is running"}


@app.on_event("startup")
async def startup_event():
    """
    Initialize services when the application starts
    """
    try:
        await rag_service.initialize_services()
        logger.info("RAG services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG services: {str(e)}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)