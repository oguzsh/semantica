# 🧠 Semantica

**Semantica** is a lightweight semantic search engine for PDF documents.
It processes PDF files, converts them into vectorized text chunks, and enables intelligent retrieval using embedding-based similarity search — all without using an LLM.

---

## 🚀 Features

* 📄 Upload any PDF file
* ✂️ Automatic chunking of document content
* 🔢 Embedding with HuggingFace (`MiniLM`)
* 🧠 Vector search with Qdrant
* ⚡ Fast and local — no OpenAI API required
* 📆 Built with FastAPI, LangChain, and Qdrant

---

## 🖥️ Tech Stack

| Layer     | Tool                                                   |
| --------- | ------------------------------------------------------ |
| Backend   | [FastAPI](https://fastapi.tiangolo.com/)               |
| Parsing   | [`pymupdf4llm`](https://pypi.org/project/pymupdf4llm/) |
| Chunking  | [`LangChain MarkdownTextSplitter`](https://python.langchain.com/api_reference/text_splitters/markdown/langchain_text_splitters.markdown.MarkdownTextSplitter.html)                       |
| Embedding | [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)               |
| Vector DB | [Qdrant](https://qdrant.tech/) via Docker              |

---

## 🔧 Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/yourname/semantica.git
cd semantica
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Qdrant locally (Docker)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Start the FastAPI server

```bash
fastapi dev main
```

Then open the Swagger UI at:
📍 `http://localhost:8000/docs`

---

## 🦪 API Endpoints

### `POST /upload`

Uploads and parses a PDF file.
Chunks it and saves to Qdrant with embeddings.

### `POST /search`

Send a semantic query and receive relevant chunks.
Example request:

```json
{
  "query": "Does this PDF mention 'fun' keyword?"
}
```

Example response:

```json
[
  {
    "score": 0.92,
    "text": "This is a simple PDF file. Fun fun fun.",
    "source_file": "sample.pdf",
    "chunk_id": 1
  }
]
```

---

## 📜 Future Plans

* [ ] LLM-based answer generation
* [ ] Multi-document support
* [ ] Frontend interface for document search (possibly separated)

---

## 🤝 Contributing

Pull requests, feedback and ideas are always welcome.
If you use this project, feel free to ⭐️ the repo and share your feedback.

---

## 📄 License

MIT
