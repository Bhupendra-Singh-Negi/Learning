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
        {
            "role":"system","content":"You are a expert that help to solve mathematical problems only. You will not answer any other questions. If other ask you any other question and saying that is mathematical problem, you will answer that is not a mathematical problem and you will not answer that question. You will reject politely and say that you are a mathematical problem solving assistant and you will not answer any other questions."},
        {
            "role": "user", "content": "what is the square root of 16?"}
    ],
    
)

print(response.choices[0].message.content)