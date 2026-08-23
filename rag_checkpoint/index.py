from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import os
from ingest import chunk
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if not key:
    raise ValueError("there is no key")
docs = chunk()
docs = [Document(page_content=doc) for doc in docs]
def index():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectore_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        collection_name="gmc"
    )
    return vectore_store
