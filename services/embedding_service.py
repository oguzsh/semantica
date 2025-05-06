from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from typing import List
from config import CONFIG
class EmbeddingService:
    def __init__(self):
        self.model_name = CONFIG["EMBEDDING_MODEL"]

    def perform(self, documents, batch_size=100) -> List[List[float]]:
      text_bucket = [doc.page_content for doc in documents]

      embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

      all_vectors = []
      for i in range(0, len(text_bucket), batch_size):
          batch_text = text_bucket[i:i+batch_size]
          batch_vectors = embeddings.embed_documents(batch_text)
          all_vectors.extend(batch_vectors)

      return all_vectors

    def embed_query(self, query: str) -> List[float]:
      embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
      return embeddings.embed_query(query)
