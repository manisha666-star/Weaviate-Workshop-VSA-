# Movie Search Application

A semantic search application for movies using Weaviate vector database and Streamlit.

## Features

- Search movies by plot, title, or theme using semantic search
- Fast and accurate movie recommendations based on content similarity
- Clean and intuitive Streamlit UI

## Setup

1. Create a `.env` file with your Weaviate credentials:
```bash
cp .env.example .env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Deployment

To deploy on Streamlit Cloud:

1. Create a Streamlit account at https://streamlit.io/cloud
2. Connect your GitHub repository
3. Configure secrets in Streamlit Cloud:
   - WEAVIATE_URL
   - WEAVIATE_API_KEY
4. Deploy with one click

## Requirements

- Python 3.8+
- Streamlit Cloud account
- Weaviate vector database
