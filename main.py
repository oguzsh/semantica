import os.path
from fastapi import FastAPI, UploadFile

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

    return {"file_name": file.filename}
  except Exception as e:
    return {"message": e.args}
