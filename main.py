import os.path
from fastapi import FastAPI, UploadFile

from config import CONFIG

from models.search_request import SearchRequest
from services.embedding_service import EmbeddingService
from services.pdf_service import PdfService
from services.qdrant_service import QdrantService

app = FastAPI()

file_save_path = os.path.join(os.getcwd(), 'temp')

# Routes
@app.get("/")
async def read_root():
  return {"message": "Hello World"}

@app.get('/health_check')
async def health_check():
  return {"status": "ok"}

@app.post('/upload')
async def upload_file(file: UploadFile):
  try:
    file_path = os.path.join(file_save_path, f"{file.filename}")
    if not os.path.exists(file_save_path):
      os.makedirs(file_save_path)

    with open(file_path, 'wb') as f:
      f.write(await file.read())

    pdf_service = PdfService(file_path)
    documents = pdf_service.process_pdf()

    embedding_service = EmbeddingService()
    embeddings = embedding_service.perform(documents)

    qdrant_service = QdrantService(collection_name=CONFIG["QDRANT_COLLECTION_NAME"])
    qdrant_service.upload_vectors(documents, embeddings)

    # Remove the uploaded file after processing
    os.remove(file_path)

    return {"file_name": file.filename}
  except Exception as e:
    return {"message": e.args}


@app.post('/search')
async def search(request: SearchRequest):
  try:
    qdrant_service = QdrantService(collection_name=CONFIG["QDRANT_COLLECTION_NAME"])
    embedding_service = EmbeddingService()
    embedding = embedding_service.embed_query(request.query)

    results = qdrant_service.search(query_vector=embedding, top_k=5)
    return {"results": results}
  except Exception as e:
    return {"message": e.args}
