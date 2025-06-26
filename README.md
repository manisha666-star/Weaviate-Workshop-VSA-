Weaviate Vector Search Application - Project Documentation

#Project Overview

Built a semantic movie search application using:
- Weaviate (vector database for semantic search)
- MongoDB (source data storage)
- Streamlit (UI for search interface)
- Sentence Transformers (embedding generation)

#Project Steps & Implementation

### 1. Setup & Configuration
- Created a Weaviate Cloud (WCS) cluster
- Set up a MongoDB Atlas database with movie data
- Configured environment variables (`.env`):
  ```ini
  # .env
  WEAVIATE_URL="8ddmcj9dsag23ej1iosta.c0.europe-west3.gcp.weaviate.cloud" 
  WEAVIATE_API_KEY="TktHUDNFNkFucWUyaVpwQl9mVmRxR3poaVZJOGhMTjdnQ2FFZHNnOFRwaTQ2UkJjM1ZWNTFUSWdjd0g0PV92MjAw"
  MONGO_URI="mongodb://localhost:27017/" 
  MONGO_DB="Moviedb"
  MONGO_COLLECTION="movies"

  ```

### 2. Data Import from MongoDB to Weaviate
- Problem: Needed to extract movie data (title, cast, crew) and generate embeddings.
- Solution: Used `pymongo` to fetch data and `sentence-transformers` to create embeddings.
- Key Code (`import_data.py`):
  ```python
  # # Import data
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
  ```

### 3. Building the Streamlit UI
- Problem: Needed an interactive search interface.
- Solution: Used Streamlit for a simple, user-friendly UI.
- Key Features:
  - Semantic search (vector similarity)
  - Display movie details (title, cast, crew, similarity score)
  - Error handling for failed queries.

### 4. Deployment to Streamlit Cloud
- Problem: Needed to host the app publicly.
- Solution: Deployed via GitHub + Streamlit Cloud.
- Steps:
  1. Pushed code to GitHub.
  2. Connected repo to Streamlit Cloud.
  3. Added `.env` secrets in Streamlit settings.
  4. Deployed with one click.


## Sample of code run locally
  ```Python
    streamlit run app.py
  ```
<img src="https://github.com/mmanisha666-star/Screenshot 2025-06-26 at 17.31.18.png?raw=true" width="500">
<img src="https://github.com/mmanisha666-star/Screenshot 2025-06-26 at 17.30.52?raw=true" width="500">
<img src="https://github.com/mmanisha666-star/Screenshot 2025-06-26 at 17.30.33.png?raw=true" width="500">
---

## Problems Faced & Solutions

### 1. Weaviate Connection Issues
- Problem: `gRPC timeout errors` when connecting to Weaviate Cloud.
- Solution:  
  - Increased timeout settings.
  - Added fallback to REST API if gRPC fails.
  - Code Fix:
    ```python
    auth = weaviate.auth.AuthApiKey(Config.WEAVIATE_API_KEY)
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=Config.WEAVIATE_URL,
        auth_credentials=weaviate.auth.AuthApiKey(Config.WEAVIATE_API_KEY),
        skip_init_checks=True  # Prevent gRPC timeout issues
    )
    ```

### 2. Schema Creation Errors
- Problem: `ValidationError` when creating Weaviate schema.
- Solution: 
  - Used proper `Property` class (not dictionaries).
  - Corrected `data_type` format (e.g., `["text"]`).
  - Code Fix:
    ```python
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "plot", "dataType": ["text"]},
        {"name": "genres", "dataType": ["text[]"]},
        {"name": "year", "dataType": ["int"]}
    ]
    ```

### 3. Missing Properties in Search Results
- Problem: `"No such prop 'title' found in class 'Movie'"`.
- Solution:  
  - Verified schema matched query fields.
  - Used `return_properties` correctly:
    ```python
    results = movie_collection.query.near_vector(
            near_vector=vector,
            limit=5,
            return_properties=["title", "overview", "genres", "release_date", "vote_average"],
            return_metadata=["distance"]
        )
    ```

### 4. Streamlit Deployment Issues
- Problem: Environment variables not loading.
- Solution:  
  - Added `secrets.toml` in Streamlit Cloud.
  - Verified `.env` was in `.gitignore`.

---

## Key Learnings

### 1. Weaviate Best Practices
- Schema design matters: Define properties correctly.
- Batch imports improve performance: Use `batch.dynamic()`.
- Hybrid search (vector + keyword) works best for some queries.

### 2. Error Handling
- Retry mechanisms are crucial for cloud connections.
- Logging helps debug issues (`logging.basicConfig(level=logging.INFO)`).

### 3. Streamlit for Rapid Prototyping
- Fast UI development with minimal code.
- Easy deployment via GitHub integration.

---

## Future Improvements
- Add filters (by year, genre, rating).
- Implement hybrid search (BM25 + vector).
- Cache embeddings for faster reloads.
- Add user feedback (thumbs up/down on results).

---

## Conclusion
This project successfully built a semantic movie search engine using Weaviate and Streamlit. Despite initial challenges with connection stability and schema setup, we implemented robust solutions for production-ready deployment.  
