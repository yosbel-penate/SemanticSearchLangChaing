from PyPDF2 import PdfReader
from src.logic.tools import *
import os

def process_query_LLM(pdf_file_path):
    os.environ["OPENAI_API_KEY"] = load_api_key()
    reader = PdfReader(pdf_file_path)
    raw_text = create_raw_text(reader)
    texts = split_text(raw_text)
    doc_search(texts, dir = os.path.dirname(pdf_file_path))

def consult_query_LLM(pdf_file_path):
    db = doc_load(pdf_file_path)
    return db
