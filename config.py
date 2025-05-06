import os

CONFIG = {
  "QDRANT_URL": os.getenv("QDRANT_URL"),
  "QDRANT_COLLECTION_NAME": "pdf_collection",
  "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2",
  "EMBEDDING_MODEL_SIZE": 384
}