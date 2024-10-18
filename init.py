from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from qdrant_client.http.models import Distance, VectorParams
import os

load_dotenv()

COLLECTION = os.getenv("COLLECTION")

print(COLLECTION)

client = QdrantClient(path="tmp/langchain-qdrant")

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)