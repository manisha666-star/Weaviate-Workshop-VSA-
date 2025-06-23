import streamlit as st
import weaviate
from sentence_transformers import SentenceTransformer
from config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Initialize clients
    client = weaviate.connect_to_wcs(
        cluster_url=Config.WEAVIATE_URL,
        auth_credentials=weaviate.auth.AuthApiKey(Config.WEAVIATE_API_KEY)
    )
    
    model = SentenceTransformer(Config.EMBEDDING_MODEL)
    logger.info("Successfully initialized Weaviate client and model")

except Exception as e:
    st.error(f"Error initializing clients: {str(e)}")
    st.info("Please check your WEAVIATE_URL and WEAVIATE_API_KEY in the .env file")
    raise

# Streamlit UI
st.title("🎬 Movie Search")
query = st.text_input("Search movies by plot, title, or theme")

if query:
    try:
        # Generate embeddings and search
        vector = model.encode(query).tolist()
        
        query = client.query.get("Movie", ["title", "plot", "genres", "year"])\
            .with_near_vector({
                "vector": vector
            })\
            .with_limit(5)
        
        results = query.do()

        if results.get("errors"):
            st.error("Error in Weaviate query:")
            for error in results["errors"]:
                st.error(f"- {error['message']}")
        else:
            movies = results["data"]["Get"]["Movie"]
            if not movies:
                st.info("No movies found matching your search criteria")
            else:
                st.success(f"Found {len(movies)} movies matching your search")
                
                for movie in movies:
                    with st.expander(f"{movie['title']} ({movie['year']})"):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            st.write(f"**Genres:** {', '.join(movie['genres'])}")
                        with col2:
                            st.write(f"**Plot:** {movie['plot']}")

    except Exception as e:
        st.error(f"Error during search: {str(e)}")
        logger.error(f"Search error: {str(e)}")