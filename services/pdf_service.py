from langchain_text_splitters import MarkdownTextSplitter
import pymupdf4llm

class PdfService:
  def __init__(self, file_path: str):
    self.file_path = file_path

  def process_pdf(self):
    parsed_pdf = self.__convert_to_markdown()
    chunks = self.__split_by_chunks(parsed_pdf)

    return chunks

  def __convert_to_markdown(self):
    parsed_pdf = pymupdf4llm.to_markdown(self.file_path)
    return parsed_pdf

  def __split_by_chunks(self, parsed_pdf: str, chunk_size: int = 500, chunk_overlap: int = 100):
    splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    splitted_data = splitter.create_documents([parsed_pdf])

    return splitted_data
