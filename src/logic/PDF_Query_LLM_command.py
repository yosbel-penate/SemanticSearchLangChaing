from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from PyPDF2 import PdfReader
from locals_variables import *
from tools import *
import os

os.environ["OPENAI_API_KEY"] = load_api_key()

reader = PdfReader(PDF_FILE)

raw_text = create_raw_text(reader)
texts = split_text(raw_text)
docsearch = doc_search(texts)

chain = load_qa_chain(OpenAI(), chain_type="stuff")

while True:
    print("\nMake you question (Control-c to Exit):")
    query = input()
    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    print("\nAnswer:")
    print(answer)