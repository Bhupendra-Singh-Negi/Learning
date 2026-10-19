from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT = """
You're an exper AI assistant in resolving user queries using chain of thought.
You work on START, PLAN AND OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN cana be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

RULES:
-Strickly follow the given JSON output format.
-Only run one step at a time.
-The sequence of steps is START(where user gives an input), PLAN (where you plan the steps to solve the problem, that can be multiple times) and finally OUTPUT (where you display the final output to user).

Output JSON Format:
{"step":"START"|"PLAN"|"OUTPUT","content":"string"}

EXAMPLE:
START: hey can you solve 2+3*5/10
PLAN: {"step":"PLAN","content":"seems like user is interesting in solving mathematical problem" }
PLAN: {"step":"PLAN","content":"Looking at the problem, we should solve this using BODMAS method" }
PLAN: {"step":"PLAN","content":"Yes, The BODMAS is correct thing to be done here" }
PLAN: {"step":"PLAN","content":"first we must multiply 3 and 5 which is 3*5=15" }
PLAN: {"step":"PLAN","content":"then we divide 15 by 10 so 15/10=1.5" }
PLAN: {"step":"PLAN","content":"then we add 2 to 1.5 so 2+1.5=3.5" }
PLAN: {"step":"PLAN","content":"finally we have the answer 3.5" }
OUTPUT: {"step":"OUTPUT","content":"Great! The answer is 3.5" }

"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type":"json_object"},
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
         },
        {
            "role": "user", "content": "write a js code to find minimum step to reach nth step if we can take steps of size 2, or 3?"
        },
        {
            "role": "assistant", "content": json.dumps({"step":"START","content":"You want a js code to find minimum step to reach nth step if we can take steps of size 2, or 3"})
        },
        {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "The user wants a JavaScript function to find the minimum steps to reach the nth step, using steps of size 2 or 3. This is a dynamic programming problem."})},
        {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "The user wants a JavaScript function `minStepsToN` that calculates the minimum number of steps to reach `n`. The allowed step sizes are 2 and 3. This is a classic dynamic programming problem."})}
    ],
    
)

print(response.choices[0].message.content)