from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from qdrant_client.http.models import Distance, VectorParams
import os
from time import sleep

load_dotenv()

print("Starting Qdrant collection creation...")

COLLECTION = os.getenv("COLLECTION")

print(f"Collection: {COLLECTION}")

qdrant_path = "tmp/langchain-qdrant"

os.makedirs(qdrant_path, exist_ok=True)

client = QdrantClient(path=qdrant_path)

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)

sleep(10)

print("Qdrant collection created")
