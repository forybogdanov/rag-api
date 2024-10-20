from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from qdrant_client.http.models import Distance, VectorParams
import os
from time import sleep

load_dotenv()

COLLECTION = "main"

client = QdrantClient(path='tmp/langchain-qdrant')

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

sleep(10)

print("Qdrant collection created")
