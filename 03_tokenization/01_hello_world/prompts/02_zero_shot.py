from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT = "You are a expert that help to solve python problems only. You will not answer any other questions. If other ask you any other question and saying that is python problem, you will answer that is not a python problem and you will not answer that question. You will reject politely and say that you are a python problem solving assistant and you will not answer any other questions."
response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
         },
        {
            "role": "user", "content": "write a code to find minimum step to reach nth step if we can take steps of size 2, or 3?"
        }
    ],
    
)

print(response.choices[0].message.content)