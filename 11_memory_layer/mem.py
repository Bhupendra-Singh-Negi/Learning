from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
OPENAI_API_KEY=os.environ["OPENROUTER_API_KEY"]

client=OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333},
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "openrouter/free",
            "api_key": OPENAI_API_KEY,
            "openai_base_url": "https://openrouter.ai/api/v1",
        },
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "gemini-embedding-2",
            "api_key": os.environ["GEMINI_API_KEY"],
            "openai_base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "embedding_dims": 1536,
        },
    },
}

memory_client = Memory.from_config(config)

while True:
    user_query=input(">  ")

    search_memory= memory_client.search( query=user_query,filters={"user_id": "bhupendra"},)

    memories=[
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results")
    ]

    print("\n found users memories:", memories)

    SYSTEM_PROMPT=f"""
        Here is the context about the user:
        {json.dumps(memories)}

        Instructions:
        - Use relevant memories when answering.
        - If the answer is not available in the memories, do not invent it.
        - Answer naturally and concisely.
    
    """
    response= client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_query}
        ]
    )

    ai_response= response.choices[0].message.content

    print("\nAI:", ai_response)

    memory_client.add(
        user_id="bhupendra",
        messages=[
            {"role":"user","content":user_query},
            {"role":"assistant","content":ai_response},
        ]
    )

    print("Memory has been saved")