from PyPDF2 import PdfReader
from src.logic.locals_variables import OPENAI_API_KEY
from src.logic.tools import *
import os

def process_query_LLM(pdf_file_path):
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    reader = PdfReader(pdf_file_path)
    raw_text = create_raw_text(reader)
    texts = split_text(raw_text)
    doc_search(texts, dir = os.path.dirname(pdf_file_path))

def consult_query_LLM(pdf_file_name):
    name = cleanFilename(pdf_file_name)
    db = doc_load(name)
    return db
