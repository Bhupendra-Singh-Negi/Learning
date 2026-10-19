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
START: you want to solve 2+3*5/10
PLAN: {"step":"PLAN","content":"seems like user is interesting in solving mathematical problem" }
PLAN: {"step":"PLAN","content":"Looking at the problem, we should solve this using BODMAS method" }
PLAN: {"step":"PLAN","content":"Yes, The BODMAS is correct thing to be done here" }
PLAN: {"step":"PLAN","content":"first we must multiply 3 and 5 which is 3*5=15" }
PLAN: {"step":"PLAN","content":"then we divide 15 by 10 so 15/10=1.5" }
PLAN: {"step":"PLAN","content":"then we add 2 to 1.5 so 2+1.5=3.5" }
PLAN: {"step":"PLAN","content":"finally we have the answer 3.5" }
OUTPUT: {"step":"OUTPUT","content":"Great! The answer is 3.5" }

"""
print("\n")
message_history = [
    {"role":"system","content":SYSTEM_PROMPT},
]

user_query =input("👉🏻:")
message_history.append({"role":"user","content":user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-3.8-flash",
        response_format={"type":"json_object"},
        messages=message_history,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})

    parsed_result = json.loads(raw_result)  

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
    elif parsed_result.get("step") == "PLAN":
        print("📝", parsed_result.get("content"))
    elif parsed_result.get("step") == "OUTPUT":
        print("✅", parsed_result.get("content"))
        break

    # gemini want last role to be user
    message_history.append({
        "role": "user",
        "content": "Continue to the next step."
    })

print("\n")
