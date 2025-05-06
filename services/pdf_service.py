from datetime import datetime
import os
from langchain.docstore.document import Document
from langchain_text_splitters import MarkdownTextSplitter
import pymupdf4llm

class PdfService:
  def __init__(self, file_path: str):
    self.file_path = file_path
    self.filename = os.path.basename(file_path)

  def process_pdf(self):
    parsed_pdf = self.__convert_to_markdown()
    chunks = self.__split_by_chunks(parsed_pdf)
    return chunks

  def __convert_to_markdown(self):
    return pymupdf4llm.to_markdown(self.file_path)

  def __split_by_chunks(self, parsed_pdf: str, chunk_size: int = 500, chunk_overlap: int = 100):
      document = Document(
          page_content=parsed_pdf,
          metadata={
              "source_file": self.filename,
              "uploaded_at": datetime.now().isoformat(),
              "file_path": self.file_path
          }
      )

      splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
      splitted_documents = splitter.split_documents([document])

      for idx, doc in enumerate(splitted_documents):
          doc.metadata["chunk_id"] = idx # For tracking

      return splitted_documents