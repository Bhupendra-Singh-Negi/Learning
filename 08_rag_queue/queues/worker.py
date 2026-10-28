from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
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

def process_query(query: str):
    print("Searching chunks", query)
    search_result = vector_db.similarity_search(query)

    context="\n\n\n".join([f"Page content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile location:{result.metadata['source']}" for result in search_result])

    SYSTEM_PROMPT =f"""
    You are a helpful AI assistant who answer user query based on the available context retrived from a PDF file along with a page_content and page number.

    You should only answer the user based on the following context and navigate the user to open the right page number to know more.
    Context:
    {context}
    """
    response= openai_client.chat.completions.create(
        model="nvidia/nemotron-3.5-super-vl:free",
        extra_body={
            "models": [
                "google/gemma-4-26b-a4b-it:free",
                "recursive/flint-v1.0:free",
                "minimax/minimax-m3.1-flash:free",
            ]
        },
        messages=[
            {"role":"system", "content":SYSTEM_PROMPT},
            {"role":"user", "content":query}
        ]
    )
    print(f"🤖: {response.choices[0].message.content}")
    return response.choices[0].message.content