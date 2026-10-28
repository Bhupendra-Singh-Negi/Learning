from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

client=OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
response = client.chat.completions.create(
    model="openrouter/free",
    extra_body={
        "models": [
            "google/gemma-4-26b-a4b-it:free",
        ]
    },
    messages=[
        {"role":"user", "content":[
            {"type":"text","text":"Generate a caption for this image in about 50 words"},
            {"type":"image_url","image_url":{"url":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80"}}
        ]}
    ]
)

print(f"🤖: {response.choices[0].message.content}")