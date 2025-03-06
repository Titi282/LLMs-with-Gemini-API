import os
# config/settings.py

# Function to read API keys and URLs
def read_secret_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None


# Set paths to secret files
# openai_api_key_file = "/run/secrets/openai_api_key"
gemini_api_key_file = "/run/secrets/gemini_api_key"
qdrant_api_key_file = "/run/secrets/qdrant_api_key"
qdrant_url_file = "/run/secrets/qdrant_url"

# Read secrets from files
# OPENAI_API_KEY = read_secret_file(openai_api_key_file)
GEMINI_API_KEY = read_secret_file(gemini_api_key_file)
QDRANT_API_KEY = read_secret_file(qdrant_api_key_file)
QDRANT_URL = read_secret_file(qdrant_url_file)

QDRANT_COLLECTION = "MyCollection"
GEMINI_EMBEDDING_MODEL = "models/embedding-001" 
GEMINI_GENERATION_MODEL = "gemini-1.5-flash"
# OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
# OPENAI_GPT_MODEL = "gpt-3.5-turbo"


# Maximum number of results for Qdrant vector database
MAX_NO_SEARCH_RESULTS_QDRANT = 9

HTTP_500_INTERNAL_SERVER_ERROR = 500
