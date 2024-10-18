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

@app.post("/collection")
async def create_collection(collection_name: str):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )
    return {"message": f"Collection {collection_name} created"}

@app.delete("/collection")
async def delete_collection(collection_name: str):
    client.delete_collection(collection_name=collection_name)
    return {"message": f"Collection {collection_name} deleted"}
