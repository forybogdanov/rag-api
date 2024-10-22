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
from langchain_text_splitters import CharacterTextSplitter
from transformers import GPT2TokenizerFast

# also works with "BAAI/bge-large-en"
# model_name = "BAAI/bge-small-en"
model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

class IngestData(BaseModel):
    files: List[str]
    dataset_id: str

class RetreiveData(BaseModel):
    prompt: str
    dataset_id: str

class DeleteData(BaseModel):
    dataset_id: str

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

    vector_store = Chroma(data.dataset_id, embeddings, "./tmp/chroma.db")

    folder_id = str(uuid.uuid4())

    os.makedirs(f"files/{folder_id}")
    for file in data.files:
        file_id = str(uuid.uuid4())
        extension = file.split(".")[-1]
        if extension not in ["pdf", "txt"]:
            continue
        response = requests.get(file)
        try :
            if extension == "txt":
                content = response.text
                text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
                    tokenizer,
                    chunk_size=10000,
                )
                texts = text_splitter.split_text(content)
                documents = []
                for text in texts:
                    document = Document(page_content=text, metadata={"dataset_id": data.dataset_id, "link": file}, id=str(uuid.uuid4()))
                    documents.append(document)
                vector_store.add_documents(documents)
            if extension == "pdf":
                    file_path = f"files/{folder_id}/{file_id}.{extension}"
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                        loader = PyPDFLoader(file_path)
                        pages = loader.load_and_split()
                        for page in pages:
                            document = Document(page_content=page.page_content, metadata={"dataset_id": data.dataset_id, "link": file}, id=str(uuid.uuid4()))
                            vector_store.add_documents([document])
        except Exception as e:
            print(e)
            continue
    return {"message": "OK"}

@app.get("/retreive/")
async def search(data: RetreiveData):
    if (data.dataset_id is None or data.dataset_id == "" or data.prompt is None or data.prompt == ""):
        return {"message": "Invalid request"}
    vector_store = Chroma(data.dataset_id, embeddings, "./tmp/chroma.db")
    results = vector_store.similarity_search(data.prompt)
    return results

@app.delete("/delete/")
async def delete(data: DeleteData):
    if (data.dataset_id is None or data.dataset_id == ""):
        return {"message": "Invalid request"}
    vector_store = Chroma(data.dataset_id, embeddings, "./tmp/chroma.db")
    vector_store.delete_collection()
    return {"message": "OK"}