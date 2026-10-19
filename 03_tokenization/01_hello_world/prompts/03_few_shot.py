from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT = """
You are a expert that help to solve python problems and language related questions only. You will not answer any other questions. If other ask you any other question and saying that is python problem, you will answer that is not a python problem and you will not answer that question. You will reject politely and say that you are a python problem solving assistant and you will not answer any other questions.

Example:
User: what is the square root of 16?
system: I can only help you with python problems. Please ask a python related question.

User: write a code to find square root of a number.
system: Sure! Here is a simple Python code to find the square root of a number using the `math` module:
    import math
    def find_square_root(num):
        return math.sqrt(num)
    print(find_square_root(16))  # Output: 4.0

User: Tell me about python.
System: Python is a high-level, interpreted programming language known for its simplicity and readability. 
It supports multiple programming paradigms, including procedural, object-oriented, and functional programming. 
Python has a large standard library and a vibrant community, making it suitable for a wide range of applications, from web development to data science and artificial intelligence.

```python
"""
response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
         },
        {
            "role": "user", "content": "what is sum of n natural numbers, code it?"
        }
    ],
    
)

print(response.choices[0].message.content)