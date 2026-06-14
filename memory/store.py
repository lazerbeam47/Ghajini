import os
from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

config={
    "llm":{
        "provider":"gemini",
        "config":{
            "model":"gemini-2.5-flash",
            "api_key":GOOGLE_API_KEY,
            "temperature":0.2,
        }
    },
    "embedder":{
        "provider":"gemini",
        "config":{
            "model":"models/gemini-embedding-001",
            "api_key":GOOGLE_API_KEY,
            "embedding_dims":768
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "ghajini",
            "path": "./data/chroma"
        }
    }
}

m=Memory.from_config(config)

def store_memory(message: str, user_id: str):
    m.add(message, filters={"user_id": user_id})

def retrieve_memory(query: str, user_id: str):
    return m.search(query, filters={"user_id": user_id})