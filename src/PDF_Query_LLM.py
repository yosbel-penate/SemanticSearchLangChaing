from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS

import os
os.environ["OPENAI_API_KEY"] = "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"

reader = PdfReader('pdf/volz_voncramon_intuitive_processes_jcn_2006.pdf')

raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

#print(texts[0])

embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts, embeddings)

docsearch.save_local('store')

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import chroma

chain = load_qa_chain(OpenAI(), chain_type="stuff")

query = "who are the authors of the article?"
docs = docsearch.similarity_search(query)
answer = chain.run(input_documents=docs, question=query)

print(answer)