Weaviate Vector Search Application - Project Documentation

#Project Overview
Built a semantic movie search application using:
- Weaviate (vector database for semantic search)
- MongoDB (source data storage)
- Streamlit (UI for search interface)
- Sentence Transformers (embedding generation)

#Project Steps & Implementation

### 1. Setup & Configuration**
- Created a Weaviate Cloud (WCS) cluster**
- Set up a MongoDB Atlas database with movie data
- Configured environment variables (`.env`):
  ```ini
  WEAVIATE_URL=https://your-cluster.weaviate.cloud
  WEAVIATE_API_KEY=your-api-key
  MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/
  MONGO_DB=Moviedb
  MONGO_COLLECTION=movies
  ```

### 2. Data Import from MongoDB to Weaviate
- Problem: Needed to extract movie data (title, cast, crew) and generate embeddings.
- Solution: Used `pymongo` to fetch data and `sentence-transformers` to create embeddings.
- Key Code (`import_data.py`):
  ```python
  # Convert MongoDB data to Weaviate format
  cast_names = [p["name"] for p in movie.get("cast", [])[:3]]
  text = f"{movie['title']} starring {', '.join(cast_names)}"
  embedding = model.encode(text).tolist()
  
  # Insert into Weaviate
  batch.add_object(
      properties={
          "movie_id": movie["movie_id"],
          "title": movie["title"],
          "cast": [p["name"] for p in movie.get("cast", [])],
          "crew": [p["name"] for p in movie.get("crew", [])],
          "combined_text": text
      },
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

---

## Problems Faced & Solutions

### 1. Weaviate Connection Issues
- Problem: `gRPC timeout errors` when connecting to Weaviate Cloud.
- Solution:  
  - Increased timeout settings.
  - Added fallback to REST API if gRPC fails.
  - Code Fix:
    ```python
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=Config.WEAVIATE_URL,
        auth_credentials=AuthApiKey(Config.WEAVIATE_API_KEY),
        skip_init_checks=True,  # Bypass gRPC check
        additional_config=weaviate.classes.init.AdditionalConfig(
            grpc_enabled=False  # Force REST
        )
    )
    ```

### 2. Schema Creation Errors
- Problem: `ValidationError` when creating Weaviate schema.
- Solution: 
  - Used proper `Property` class (not dictionaries).
  - Corrected `data_type` format (e.g., `DataType.TEXT`).
  - Code Fix:
    ```python
    properties = [
        Property(name="title", data_type=DataType.TEXT),
        Property(name="cast", data_type=DataType.TEXT_ARRAY),
    ]
    ```

### 3. Missing Properties in Search Results
- Problem: `"No such prop 'title' found in class 'Movie'"`.
- Solution:  
  - Verified schema matched query fields.
  - Used `return_properties` correctly:
    ```python
    results = movies.query.near_vector(
        near_vector={"vector": embedding},
        return_properties=["title", "cast", "crew"],
        limit=5
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
