from PyPDF2 import PdfReader
from src.logic.locals_variables import PDF_STORE_DIRECTORY, OPENAI_API_KEY
from src.logic.tools import *
import os

def process_query_LLM(pdf_file_name):
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    PDF_FILE = os.path.join(PDF_STORE_DIRECTORY, pdf_file_name)
    reader = PdfReader(PDF_FILE)
    raw_text = create_raw_text(reader)
    texts = split_text(raw_text)
    doc_search(texts, pdf_file_name)