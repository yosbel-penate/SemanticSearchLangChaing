from PyPDF2 import PdfReader
from src.logic.locals_variables import OPENAI_API_KEY
from src.logic.tools import *
import os

def cleanFilename(sourcestring,  removestring =" %:/,.\\[]<>*?-"):
    return ''.join([c for c in sourcestring if c not in removestring])

def process_query_LLM(dir, pdf_file_name):
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    PDF_FILE = dir +'/'+ pdf_file_name
    reader = PdfReader(PDF_FILE)
    raw_text = create_raw_text(reader)
    texts = split_text(raw_text)
    vectorName = cleanFilename(pdf_file_name)
    doc_search(texts, vectorName)

def consult_query_LLM(pdf_file_name):
    name = cleanFilename(pdf_file_name)
    db = doc_load(name)
    return db
