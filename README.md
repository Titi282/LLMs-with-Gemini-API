## Description

This project implements an LLM-powered Q&A mechanism to answer questions on public companies and their stock. We use Retrieval-Augmenting Generation (RAG) model together with Gemini APIs. The backend is implemented using FastAPI and the frontend is implemented using Streamlit. Qdrant 
cloud is used as the vector database.


## Endpoints (FastAPI)
- `/query`: 
    - **Method**: POST
    - **Input**: JSON {"question": "your question"}
    - **Output**: JSON {"answer": "returned answer"}

## Prerequisites
- Docker
- Docker Compose

## Installation and Run
1. Clone the git repository from github:
    ```bash
    git clone git@github.com:Titi282/LLMs-with-Gemini-API.git
    ```
2. Navigate to the project directory:
    ```bash
    cd dp_lab2
    ```
3. Initialize Docker Swarm
    ```bash
    docker swarm init
    ```
4. Create Docker Secrets
    ```bash
    echo "your-gemini-api-key" | docker secret create gemini_api_key -
    echo "your-qdrant-api-key" | docker secret create qdrant_api_key -
    echo "your-qdrant-url" | docker secret create qdrant_url -
    ```
    Add ```echo "your-openai-api-key" | docker secret create openai_api_key - ``` if use Openai API

    Verify Created Secrets : ```docker secret ls```

5. Run the following command to start the services:
    ```bash
    docker compose up --build
    ```

6. The backend uses port `8000`, and the frontend (Streamlit app) uses port `8501`.

## Configuration
- **Environment Variables**:
    - `OPENAI_API_KEY`: API key for Open AI.
    - `QDRANT_API_KEY`: API key for Qdrant.
    - `QDRANT_URL`: URL of the Qdrant vector database.
    - The API keys are stored in the following directory
        ```CSS
        ├── secrets
        │   ├── openai_api_key.secret
        │   ├── qdrant_api_key.secret
        │   └── qdrant_url.secret
        ```

## Usage
1. From your web browser, type `http://localhost:8501` .
2. A web page will show, there's an input box where you can enter your question.
3. Press Enter, the system will get the answer and show below the header "Answer"
4. You can also go to `http://localhost:8000/docs` to test the APIs
5. The notebook used to divide the pdf into chunks, get embeddings, and populate Qdrant database is Rag_Data/qa_data_prep.ipynb


## Directory Tree
```CSS
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
├── secrets
│   ├── gemini_api_key.secret
│   ├── qdrant_api_key.secret
│   └── qdrant_url.secret
├── QA_Data
│   ├── data.pdf
│   ├── qa_data_prep.ipynb
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── endpoints
│   │       ├── __init__.py
│   │       └── rag.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── frontend
│   │   ├── __init__.py
│   │   ├── main.py
│   └── services
│       ├── __init__.py
│       ├── prompt_services.py


```

<p align="center"><img src="https://github.com/Titi282/LLMs-with-Gemini-API/blob/main/images/Screenshot%202025-03-06%20213919.png" width="300"></p>
<p align="center"><img src="https://github.com/Titi282/LLMs-with-Gemini-API/blob/main/images/Screenshot%202025-03-06%20234105.png" width="300"></p>
<p align="center"><img src="https://github.com/Titi282/LLMs-with-Gemini-API/blob/main/images/Screenshot%202025-03-06%20235542.png" width="300"></p>
