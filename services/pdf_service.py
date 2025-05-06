import pymupdf4llm

class PdfService:
  def __init__(self, file_path: str):
    self.file_path = file_path

  def convert_to_markdown(self):
    parsed_pdf = pymupdf4llm.to_markdown(self.file_path, page_chunks=True)
    return parsed_pdf
