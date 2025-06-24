import streamlit as st
import weaviate
from sentence_transformers import SentenceTransformer
from config import Config
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Weaviate and embedding model
try:
    auth = weaviate.auth.AuthApiKey(Config.WEAVIATE_API_KEY)
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=Config.WEAVIATE_URL,
        auth_credentials=auth,
        skip_init_checks=True  # Prevent gRPC timeout issues
    )
    model = SentenceTransformer(Config.EMBEDDING_MODEL)
    logger.info("✅ Successfully initialized Weaviate client and model")
except Exception as e:
    st.error("❌ Failed to connect to Weaviate or load model.")
    st.stop()

# Streamlit UI
st.title("🎬 Semantic Movie Search")
st.write("Search for movies using natural language queries.")

query = st.text_input("Enter your search query:", placeholder="e.g. epic science fiction with aliens")

if query:
    try:
        # Get the collection
        movie_collection = client.collections.get("Movie")

        # Generate embedding
        vector = model.encode(query).tolist()

        # Perform semantic search
        results = movie_collection.query.near_vector(
            near_vector=vector,
            limit=5,
            return_properties=["title", "overview", "genres", "release_date", "vote_average"],
            return_metadata=["distance"]
        )

        if not results.objects:
            st.warning("No movies found matching your query.")
        else:
            st.success(f"Found {len(results.objects)} result(s):")
            for obj in results.objects:
                props = obj.properties
                st.subheader(props.get("title", "Untitled"))
                st.write(f"**Score:** {obj.metadata.distance:.4f}")
                st.write(f"**Release Date:** {props.get('release_date', 'N/A')}")
                st.write(f"**Genres:** {', '.join(props.get('genres', []))}")
                st.write(f"**Overview:** {props.get('overview', 'No overview available.')}")
                st.markdown("---")

    except Exception as e:
        logger.error(f"Search error: {e}")
        st.error(f"Search error: {str(e)}")

# Clean up
client.close()
