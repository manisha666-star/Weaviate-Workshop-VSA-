import os
import weaviate
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from config import Config
from tqdm import tqdm

# Initialize clients
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB]
collection = db[Config.MONGO_COLLECTION]

weaviate_client = weaviate.Client(
    url=Config.WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=Config.WEAVIATE_API_KEY)
)

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define Weaviate schema
class_obj = {
    "class": "Movie",
    "vectorizer": "none",
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "plot", "dataType": ["text"]},
        {"name": "genres", "dataType": ["text[]"]},
        {"name": "year", "dataType": ["int"]}
    ]
}

if not weaviate_client.schema.contains(class_obj):
    weaviate_client.schema.create_class(class_obj)

# Import data
batch_size = 50
movies = collection.find().limit(1000)  # Adjust limit as needed

for movie in tqdm(movies, desc="Importing to Weaviate"):
    text = f"{movie['title']}: {movie.get('plot', '')}"
    embedding = model.encode(text).tolist()
    
    weaviate_client.data_object.create(
        data_object={
            "title": movie["title"],
            "plot": movie.get("plot", ""),
            "genres": movie.get("genres", []),
            "year": movie.get("year", 0)
        },
        class_name="Movie",
        vector=embedding
    )

print("✅ Data import completed!")