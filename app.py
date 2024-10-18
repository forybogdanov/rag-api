import os
from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_DOMAIN = os.getenv("QDRANT_DOMAIN")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

client = QdrantClient(url=QDRANT_DOMAIN)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/create-collection")
async def create_collection():
    client.recreate_collection(collection_name="collection 1")
    return {"message": "Collection created"}


