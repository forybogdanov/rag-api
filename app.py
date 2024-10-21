import os
from typing import List
from fastapi import FastAPI
from langchain_core.documents import Document
import uuid
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
import requests
from langchain_chroma import Chroma

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
    # TODO: add metadata
    # metadata: dict = {}

class RetreiveData(BaseModel):
    prompt: str
    dataset_id: str
    # TODO: add top_k
    # top_k: int = 5
    # TODO: add filters

# chroma_client = chromadb.PersistentClient("./tmp/chroma.db")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ok"}

@app.get("/health")
async def health():
    return {"message": "OK"}

@app.post("/ingest/")
async def ingest(data: IngestData):
    if (data.dataset_id is None or data.dataset_id == "" or data.files is None):
        return {"message": "Invalid request"}

    # collection = chroma_client.get_or_create_collection(data.dataset_id)
    vector_store = Chroma(data.dataset_id, embeddings, "./tmp/chroma.db")

    folder_id = str(uuid.uuid4())

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
            if extension == "txt":
                with open(filepath, "r") as f:
                    content = f.read()
                document = Document(page_content=content, metadata={"dataset_id": data.dataset_id, "link": file}, id=file_id)
                vector_store.add_documents([document])
            elif extension == "pdf":
                loader = PyPDFLoader(filepath)
                pages = loader.load_and_split()
                for page in pages:
                    document = Document(page_content=page.page_content, metadata={"dataset_id": data.dataset_id, "link": file}, id=str(uuid.uuid4()))
                    vector_store.add_documents([document])
            else:
                continue
    return {"message": "OK"}

@app.get("/retreive/")
async def search(data: RetreiveData):
    if (data.dataset_id is None or data.dataset_id == "" or data.prompt is None or data.prompt == ""):
        return {"message": "Invalid request"}
    vector_store = Chroma(data.dataset_id, embeddings, "./tmp/chroma.db")
    results = vector_store.similarity_search(data.prompt)
    return results