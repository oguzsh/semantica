import os
from typing import List
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain.docstore.document import Document

DEFAULT_VECTOR_SIZE = 384 # all-MiniLM-L6-v2 output size

class QdrantService:
  def __init__(self, collection_name: str, vector_size: int = DEFAULT_VECTOR_SIZE):
    self.client = QdrantClient(url=os.getenv("QDRANT_URL"))
    self.collection_name = collection_name
    self.vector_size = vector_size

    if not self.client.collection_exists(self.collection_name):
      self.client.create_collection(
        collection_name=self.collection_name,
        vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
      )

  def upload_vectors(self, documents: List[Document], embeddings: List[List[float]]):
    if len(documents) != len(embeddings):
      raise ValueError("Documents and embeddings must have the same length")

    points = []

    for document, vector in zip(documents, embeddings):
      payload = document.metadata.copy()
      payload["text"] = document.page_content
      chunk_id = str(uuid.uuid4())

      points.append(PointStruct(
        id=chunk_id,
        vector=vector,
        payload=payload
      ))

    try:
      self.client.upsert(
        collection_name=self.collection_name,
        points=points
      )
    except Exception as e:
      print(f"Error writing points to collection {self.collection_name}: {e}")



  def search(self, query_vector: List[float], top_k: int = 5) -> List[dict]:
        if not query_vector or not isinstance(query_vector, list):
          raise ValueError("Invalid query vector")

        # Return chunks that are most similar to the query vector
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )

        if not search_result:
            return []

        results = []
        for result in search_result:
            if not result.payload:
                continue

            # Skip results with low similarity score (0.35)
            if result.score <= 0.35:
                continue

            results.append({
                "score": getattr(result, "score", 0.0),
                "text": result.payload.get("text", ""),
                "source_file": result.payload.get("source_file"),
                "chunk_id": result.payload.get("chunk_id")
            })

        return results