# services/prompt_services.py
import google.generativeai as genai
from fastapi import HTTPException
from qdrant_client import QdrantClient
from src.config.settings import HTTP_500_INTERNAL_SERVER_ERROR
from src.config.settings import MAX_NO_SEARCH_RESULTS_QDRANT
from src.config.settings import QDRANT_COLLECTION
from ratelimit import limits, sleep_and_retry
import time

CALLS_PER_MINUTE = 60  # Điều chỉnh theo giới hạn Gemini nếu cần
PERIOD = 60  # 1 phút

class PromptServices:
    """
    Class handling various prompt services related operations using Gemini.
    """

    def __init__(self,
                 gemini_api_key,
                 qdrant_url,
                 qdrant_api_key,
                 gemini_embedding_model,
                 gemini_generation_model):  # Thêm mô hình generation
        self._gemini_api_key = gemini_api_key
        self._qdrant_url = qdrant_url
        self._qdrant_api_key = qdrant_api_key
        self._gemini_embedding_model = gemini_embedding_model
        self._gemini_generation_model = gemini_generation_model
        genai.configure(api_key=self._gemini_api_key)
        self._qdrant_client = QdrantClient(host=self._qdrant_url,
                                           api_key=self._qdrant_api_key)
        self._system_prompt = ("You are an assistant with knowledge of financial market. "
                               "Please use the provided context to answer the question. "
                               "Use as much information from the context as possible. "
                               "If you do not have the information, "
                               "please do not make up the answer.")

    #############################################
    def get_embedding(self, query):
        try:
            embedding_response = genai.embed_content(
                model=self._gemini_embedding_model,
                content=query,
                task_type="retrieval_document"
            )
            return embedding_response['embedding']
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Embedding error: {str(e)}")

    #############################################
    def get_context(self, embedding, number_of_points):
        try:
            search_results = self._qdrant_client.search(
                collection_name=QDRANT_COLLECTION,
                query_vector=embedding,
                limit=number_of_points
            )
            return search_results
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Qdrant search error: {str(e)}")

    #############################################
    @sleep_and_retry
    @limits(calls=CALLS_PER_MINUTE, period=PERIOD)
    def call_gemini_api(self, query, context):
        try:
            model = genai.GenerativeModel(self._gemini_generation_model)
            prompt = f"{self._system_prompt}\n\nContext:\n{context}\n\nQuestion:\n{query}"
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Gemini API error: {str(e)}")

    #############################################
    def get_response_closest_points(self, query, search_results):
        context = ""
        for result in search_results:
            context += result.payload['text'] + "\n"

        if not context:
            return "No relevant information found in the database."

        return self.call_gemini_api(query, context)

    #############################################
    def get_response_consecutive_points(self, query, search_results):
        if not search_results:
            return "No relevant information found in the database."

        qdrant_id = search_results[0].id
        print("Qdrant ID: ", qdrant_id)
        
        half_number_of_points = MAX_NO_SEARCH_RESULTS_QDRANT // 2
        search_results = self._qdrant_client.retrieve(
            collection_name=QDRANT_COLLECTION,
            ids=list(range(max(0, qdrant_id - half_number_of_points),
                           qdrant_id + half_number_of_points + 1))
        )

        context = ""
        for result in search_results:
            context += result.payload['text'] + "\n"

        if not context:
            return "No relevant information found in the database."

        return self.call_gemini_api(query, context)