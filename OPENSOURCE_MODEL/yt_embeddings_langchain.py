import os
import sys 
from langchain.document_loaders import TextLoader
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
sys.path.append('/home/pc-116/newchatbotst')
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
from langchain.cache import SQLiteCache,InMemoryCache
langchain.llmcache = SQLiteCache(database_path=".opensource.db")
loader = TextLoader('DATA/mm.txt') 
documents = loader.load()

# Text Splitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10,separators=["\n"])
docs = text_splitter.split_documents(documents)

# embeddings = HuggingFaceEmbeddings()
from embeddings import db
db = db

from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

llm=HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.2, "max_length":200})
#google/flan-t5-xxl
chain = load_qa_chain(llm, chain_type="stuff")
def get_answer(query):
    docs = db.similarity_search(query)
    return chain.run(input_documents=docs, question=query)

