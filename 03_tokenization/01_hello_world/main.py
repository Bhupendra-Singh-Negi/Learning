from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[
        {"role": "user", "content": "Tell me 10 joke about a computer programmer."}
    ],
    
)

print(response.choices[0].message.content)