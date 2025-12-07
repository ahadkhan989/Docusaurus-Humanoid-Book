# rag-api.py
# This script is a conceptual implementation of the RAG Query API using FastAPI.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import qdrant_client
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "ai_native_textbook"

# --- FastAPI App ---
app = FastAPI(
    title="AI-Native Textbook RAG API",
    description="An API for querying the AI-Native Textbook using a RAG pipeline.",
    version="1.0.0",
)

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    query: str
    session_id: str | None = None
    selected_text: str | None = None

class QueryResponse(BaseModel):
    response: str
    cited_chapter: str
    confidence_score: float

def get_qa_chain():
    """
    Initializes and returns the RetrievalQA chain.
    """
    # Initialize Qdrant client
    client = qdrant_client.QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Initialize Qdrant vector store
    vector_store = Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings,
    )

    # Initialize the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=OPENAI_API_KEY
        ),
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
    )
    return qa_chain

qa_chain = get_qa_chain()

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """
    Receives a user query. If selected_text is provided, it uses that as context.
    Otherwise, it retrieves relevant context from the vector store and generates a response.
    """
    try:
        if request.selected_text:
            print("Selected-text-only mode activated.")
            # In this mode, we use the selected text as the context directly,
            # instead of retrieving from the vector store.
            # This is a conceptual implementation. A real implementation might
            # use a different chain or prompt template.
            
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            
            prompt_template = """Use the following context to answer the question at the end.
            
            Context: {context}
            
            Question: {question}
            
            Answer:"""
            
            prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
            chain = LLMChain(llm=llm, prompt=prompt)
            
            result = chain.run(context=request.selected_text, question=request.query)
            
            return QueryResponse(
                response=result,
                cited_chapter="User-provided text",
                confidence_score=0.99, # High confidence as it's from user text
            )

        # Get response from the QA chain
        result = qa_chain({"query": request.query})
        
        response_text = result["result"]
        
        source_docs = result.get("source_documents", [])
        cited_chapter = "Unknown"
        if source_docs:
            metadata = source_docs[0].metadata
            cited_chapter = metadata.get("source", "Unknown")

        confidence_score = 0.95 # Placeholder

        return QueryResponse(
            response=response_text,
            cited_chapter=cited_chapter,
            confidence_score=confidence_score,
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    # This would not be run directly. Use `uvicorn rag_api:app --reload`
    print("Conceptual RAG API")
    print("This script defines a FastAPI application with a /chat endpoint.")
    print("Run with: uvicorn rag_api:app --reload")
