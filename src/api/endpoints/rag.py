# src/api/endpoints/rag.py
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
from src.config.settings import *
from src.services.prompt_services import PromptServices
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InputData(BaseModel):
    input_text: str

router = APIRouter()

prompt_services = PromptServices(
    gemini_api_key=GEMINI_API_KEY,
    qdrant_url=QDRANT_URL,
    qdrant_api_key=QDRANT_API_KEY,
    gemini_embedding_model=GEMINI_EMBEDDING_MODEL, 
    gemini_generation_model= GEMINI_GENERATION_MODEL
)

def get_answer_from_llm(query):
    try:
        embedding = prompt_services.get_embedding(query)
        logger.info(f"Embedding dimension: {len(embedding)}")
        
        search_results = prompt_services.get_context(embedding, 1)
        logger.info(f"Search results: {search_results}")
        
        response = prompt_services.get_response_consecutive_points(query, search_results)
        logger.info(f"Response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in get_answer_from_llm: {e}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/query")
async def ask(question: InputData):
    response = get_answer_from_llm(question.input_text)
    return {"answer": response}

app = FastAPI()
app.include_router(router)