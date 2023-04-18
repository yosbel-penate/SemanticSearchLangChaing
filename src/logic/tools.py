from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os

def create_raw_text(reader):
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text

def split_text(raw_text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)
    return texts

def doc_search(texts, dir, name = 'index'):
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    docsearch.save_local(dir, name)
    return docsearch

def doc_load(index_name):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local('store', embeddings, index_name)

def cleanFilename(sourcestring,  removestring =" %:/,.\\[]<>*?-"):
    return ''.join([c for c in sourcestring if c not in removestring])

def get_files_in_subdir(path_to_directory, extension_file):
    pdf_files = []
    for root, dirs, files in os.walk(path_to_directory):
        for file in files:
            if file.endswith(extension_file):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def create_directory_if_it_doesnot_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)