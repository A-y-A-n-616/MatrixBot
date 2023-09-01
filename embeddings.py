from langchain.document_loaders import TextLoader
loader = TextLoader('DATA/mm.txt') 
documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
def split_docs(documents,chunk_size=500,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap
  )
  docs = text_splitter.split_documents(documents)
  return docs
docs = split_docs(documents)

from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")
print("I am under embedddings")
from langchain.vectorstores import FAISS
db = FAISS.from_documents(docs, embeddings)

