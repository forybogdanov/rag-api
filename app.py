import os
from typing import List
from fastapi import FastAPI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
from langchain_core.documents import Document
import uuid
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
import urllib.request
import requests

# TODO: try large model
model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

class IngestData(BaseModel):
    files: List[str]
    dataset_id: str

class RetreiveData(BaseModel):
    prompt: str
    dataset_id: str

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

@app.post("/ingest/")
async def ingest(data: IngestData):
    # embedding = embeddings.embed_query(data.text)
    folder_id = str(uuid.uuid4())
    if (data.files.count == 0):
        return {"message": "No files to ingest"}
    os.makedirs(f"files/{folder_id}")
    for file in data.files:
        file_id = str(uuid.uuid4())
        extension = file.split(".")[-1]
        if extension not in ["pdf", "txt"]:
            continue
        filepath = f"files/{folder_id}/{file_id}.{extension}"
        response = requests.get(file)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        match extension:
            case "txt":
                with open(filepath, "r") as f:
                    content = f.read()
                document = Document(page_content=content, metadata={"dataset_id": data.dataset_id, "link": file}, id=file_id)
                vector_store.add_documents([document])
            case "pdf":
                loader = PyPDFLoader(filepath)
                pages = loader.load_and_split()
                for page in pages:
                    document = Document(page_content=page.page_content, metadata={"dataset_id": data.dataset_id, "link": file}, id=page.id)
                    vector_store.add_documents([document])
    return {"message": "OK"}

@app.get("/retreive/")
async def search(data: RetreiveData):
    results = vector_store.search(data.prompt, "similarity")
    return results