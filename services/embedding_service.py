import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class EmbeddingService:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"

    def perform(self, documents, batch_size=100):
        text_bucket = []
        metadata_bucket = []

        for document in documents:
            text_bucket.append(document.page_content)
            metadata_bucket.append(document.metadata)

        embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

        all_vectors =[]
        for i in range(0, len(text_bucket), batch_size):
            batch_text = text_bucket[i:i+batch_size]
            batch_vectors = embeddings.embed_documents(batch_text)
            all_vectors.extend(batch_vectors)

        return list(zip(all_vectors, metadata_bucket))
