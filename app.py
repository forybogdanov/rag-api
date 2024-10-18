import os
from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
from langchain_core.documents import Document
import uuid

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION = os.getenv("COLLECTION")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

client = QdrantClient(path="tmp/langchain-qdrant")

if client.get_collection(collection_name=COLLECTION) is None:
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )

vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION,
    embedding=embeddings,
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/collection")
async def get_collection(collection_name: str):
    return {"message": f"Collection {vector_store.collection_name} retrieved"}


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

@app.post("/collection/add")
async def add_to_collection(text: str):
    print(text)
    document_1 = Document(
    page_content=text,
    metadata={"source": "user"},
    )
    docs = [document_1]
    ids = [str(uuid.uuid4()) for _ in docs]
    vector_store.add_documents(documents=docs, ids=ids)
    return {"message": f"Point added to collection {vector_store.collection_name}"}

@app.post("/collection/query")  
async def query_collection(query: str):
    docs = vector_store.similarity_search(query)
    return {"message": f"Query {query} executed", "docs": docs}

