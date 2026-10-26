from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
from pathlib import Path
from openai import OpenAI

load_dotenv()

openai_client= OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-small", 
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

vector_db= QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

# take user query
user_query=input("Ask something about DBMS: ")

# Retriving relevant chunks from vector db
search_result = vector_db.similarity_search(user_query)

context="\n\n\n".join([f"Page content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile location:{result.metadata['source']}" for result in search_result])

BASE_DIR=Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH=BASE_DIR/"system_prompt.txt"

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").format(context=context)

response= openai_client.chat.completions.create(
    model="nvidia/nemotron-3.5-super-vl:free",
    extra_body={
        "models": [
            "recursive/flint-v1.0:free",
            "minimax/minimax-m3.1-flash:free",
            "google/gemma-4-26b-a4b-it:free",
        ]
    },
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role":"user", "content":user_query}
    ]
)

print(f"🤖: {response.choices[0].message.content}")
