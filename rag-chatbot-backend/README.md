# RAG Chatbot Backend

A Retrieval-Augmented Generation (RAG) chatbot backend built with FastAPI for a Docusaurus-based AI/Robotics textbook. This backend enables users to ask questions about book content and selected text portions, leveraging vector search for relevant context retrieval.

## Features

- **Document Ingestion**: API endpoints to upload and process book content (markdown files)
- **Vector Storage**: Uses Qdrant Cloud for semantic search of document chunks
- **PostgreSQL Integration**: Stores metadata, chat history, and user sessions
- **RAG Endpoints**:
  - General chat about entire book content
  - Chat about user-selected text
- **Context Management**: Maintains conversation history and context
- **CORS Support**: Configured for Docusaurus frontend integration

## Tech Stack

- **Backend**: FastAPI (Python)
- **Embeddings**: OpenAI API
- **Vector Database**: Qdrant Cloud (Free Tier)
- **Database**: Neon Serverless Postgres
- **Python Libraries**: openai, qdrant-client, asyncpg, pydantic

## Prerequisites

- Python 3.8+
- OpenAI API Key
- Qdrant Cloud account and API key
- Neon Serverless Postgres database URL

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rag-chatbot-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your:
- OpenAI API Key
- Qdrant URL and API Key
- PostgreSQL Database URL

### 5. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /api/health` - Verify the backend is running

### Chat Endpoints
- `POST /api/chat` - General chat about book content
- `POST /api/chat-selection` - Chat about user-selected text

### Document Ingestion
- `POST /api/ingest` - Upload and process document content
- `POST /api/ingest-file` - Upload and process document file

### Sources
- `GET /api/sources` - Retrieve sources used for answers

## API Usage Examples

### Ingest Document Content
```bash
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your document content here...",
    "document_title": "Document Title",
    "document_url": "https://example.com/doc"
  }'
```

### General Chat
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the key concepts in robotics?",
    "session_id": "session123",
    "top_k": 5
  }'
```

### Chat About Selected Text
```bash
curl -X POST "http://localhost:8000/api/chat-selection" \
  -H "Content-Type: application/json" \
  -d '{
    "selected_text": "The robot uses sensors to perceive its environment...",
    "question": "How does the robot process sensor data?",
    "session_id": "session123"
  }'
```

## Project Structure

```
/rag-chatbot-backend
  /app
    main.py                 # FastAPI application entry point
    /routers
      chat.py              # Chat endpoints
      ingest.py            # Ingestion endpoints
    /services
      rag_service.py       # Main RAG orchestration
      embeddings.py        # OpenAI embeddings
      vector_store.py      # Qdrant operations
      database.py          # PostgreSQL operations
    /models
      schemas.py           # Pydantic models
    /utils
      config.py            # Configuration and environment variables
  requirements.txt         # Python dependencies
  .env.example            # Environment variables template
  .env                    # Environment variables
  README.md               # This file
```

## Configuration

The application can be configured via environment variables:

- `CHUNK_SIZE`: Size of text chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `MAX_CONTEXT_LENGTH`: Maximum context length (default: 3000)

## Error Handling

The application includes comprehensive error handling:
- Validation of required environment variables
- Proper exception handling with logging
- HTTP error responses with appropriate status codes

## Security

- CORS middleware configured for frontend integration
- Environment variables for sensitive credentials
- Input validation using Pydantic models

## License

[Specify your license here]