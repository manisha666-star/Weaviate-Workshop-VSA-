# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    # Weaviate Configuration
    WEAVIATE_URL = os.getenv("WEAVIATE_URL")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
    
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB = os.getenv("MONGO_DB", "movie_db")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "movies")
    
    # Embeddings Model
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"