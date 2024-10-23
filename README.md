# README: Retrieval-Augmented Generation (RAG) API

This project is a **Retrieval-Augmented Generation (RAG) API** built using FastAPI, LangChain, and Chroma for document ingestion and retrieval. The API allows users to upload files (PDFs and text files), process them, store them in a vector database, and retrieve relevant documents based on a search query. Embeddings are generated using the HuggingFace `bge-small-en` model.

## Features
1. **Document Ingestion**: Upload text or PDF files, split them into smaller chunks, generate embeddings, and store them in a Chroma vector store.
2. **Search/Retreival**: Retrieve the most relevant document chunks based on a query using similarity search.
3. **Delete Data**: Remove an entire dataset from the vector store.

4 **OCR PDF**: Extract text from PDF files using OCR.

## Python Packages
- `fastapi`: For building the API.
- `uvicorn`: ASGI server to run FastAPI.
- `langchain`: For document processing and embeddings.
- `langchain-chroma`: Integration of Chroma with LangChain for vector storage.
- `requests`: For downloading files from URLs.
- `pydantic`: Data validation and settings management using Python type annotations.
- `transformers`: Hugging Face model for tokenization.
- `Chroma`: Vector store for similarity search.
- `PyPDFLoader`: For loading and splitting PDF documents.

## Setup and Installation

1. **Clone the Repository**

```bash
git clone <repository-url>
cd <repository-directory>
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the API**

Use `uvicorn` to start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Health Check
**Endpoint**: `GET /health`  
**Description**: Returns a message indicating that the API is running.  

**Response**:
```json
{
    "message": "OK"
}
```

### 2. Document Ingestion
**Endpoint**: `POST /ingest/`  
**Description**: Ingest text and PDF files, split them into smaller chunks, and store them in the Chroma vector store.  

**Request Body**:
```json
{
    "files": ["<URL-of-file>"],
    "dataset_id": "<unique-dataset-id>",
    // metadata is optional dictionary
    "metadata": {"key": "value"}
}
```

**Response**:
```json
{
    "message": "OK"
}
```

### 3. Document Retrieval
**Endpoint**: `GET /retrieve/`  
**Description**: Retrieve relevant document chunks based on a search query.  

**Request Body**:
```json
{
    "prompt": "<search-query>",
    "dataset_id": "<unique-dataset-id>",
    // optional default set to 3
    "top_k": "<number>",
    // optional filter dictionary based on metadata
    "filter": {"key": "value"}
}
```

**Response**:
A list of matching document chunks is returned based on similarity search.

### 4. Delete Dataset
**Endpoint**: `DELETE /delete/`  
**Description**: Delete all documents from the vector store related to a specific dataset ID.

**Request Body**:
```json
{
    "dataset_id": "<unique-dataset-id>"
}
```

**Response**:
```json
{
    "message": "OK"
}
```

## Key Components

- **Document Ingestion**: Supports PDF and text files. Text files are split into smaller chunks based on tokenization. PDF files are processed using `PyPDFLoader`.
- **Embeddings**: HuggingFace `bge-small-en` model is used to generate embeddings for the document chunks.
- **Vector Store**: Chroma is used as a vector store to store embeddings and perform similarity search.
- **Text Splitting**: The text is split using a tokenizer to ensure each chunk fits within a specific token limit.

## File Structure

```
.
├── app.py            # The app API code
├── requirements.txt   # Required Python packages
└── files/             # Folder for temporarily storing downloaded files
```

## Future Improvements

- **Chunk size customization**: Allow custom chunk sizes during ingestion.
