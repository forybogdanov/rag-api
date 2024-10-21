import os
from fastapi import FastAPI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
from langchain_core.documents import Document
import uuid
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# TODO: try large model
model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

load_dotenv()

app = FastAPI()

COLLECTION = os.getenv("COLLECTION")

client = QdrantClient(path="tmp/langchain-qdrant")

vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION,
    embedding=embeddings,
)

@app.get("/")
async def root():
    return {"message": "ok"}

@app.get("/health")
async def health():
    return {"message": "OK"}

@app.post("/embed")
async def embed(text: str):
    embedding = embeddings.embed_query(text)
    return {"message": embedding}
