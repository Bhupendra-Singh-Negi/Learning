from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

pdf_path=Path(__file__).parent/"DBMS_Notes.pdf"

# load file 
loader= PyPDFLoader(file_path=pdf_path)
docs=loader.load()

# split doc into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=30,
)

chunks= text_splitter.split_documents(documents=docs)

# vector embedding
embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-small", 
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

print("Indexing of documents done..")