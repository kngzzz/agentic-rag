from fastapi import APIRouter, HTTPException # Removed Depends
# from core.database import get_db, WeaviateDBService # Removed
from backend.services import agent_service # Ensure backend. prefix
from backend.schemas.document import QueryRequest, QueryResponse # Ensure backend. prefix

router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest
    # db: WeaviateDBService = Depends(get_db) # Removed
):
    """
    Endpoint to ask a question to the JARVIS agent using Weaviate backend.
    The agent will use the ingested documents to formulate an answer.
    """
    try:
        print(f"Received question: {request.question}")
        # Call answer_question without the db argument
        answer, sources, thought_process = await agent_service.answer_question(request.question)
        print(f"Generated answer: {answer}")
        return QueryResponse(answer=answer, sources=sources, thought_process=thought_process)
    except ConnectionError as ce: # Added to catch Weaviate connection issues from underlying services
        print(f"Connection error during question answering: {ce}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: Could not connect to Weaviate. {ce}")
    except Exception as e:
        print(f"Error during question answering: {e}")
        # Log the full error details here in a real application
        raise HTTPException(status_code=500, detail=f"Internal server error answering question: {e}")
