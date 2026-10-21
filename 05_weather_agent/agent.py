from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import requests

load_dotenv()
client = OpenAI(
   base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY")
)

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response=requests.get(url)

    if response.status_code==200:
        return f"The weather in {city} is {response.text}"

    return "Sorry, Something went wrong"

available_tool={"get_weather":get_weather}

BASE_DIR=Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH=BASE_DIR/"system_prompt.txt"

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

print("\n")
message_history = [
    {"role":"system","content":SYSTEM_PROMPT},
]

while True:

    user_query =input("👉🏻:")
    message_history.append({"role":"user","content":user_query})

    while True:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3.5-super-vl:free",
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

        elif parsed_result.get("step")=="TOOL":
            tool_to_call=parsed_result.get("tool")
            tool_input=parsed_result.get("input")
            print("🔨", {tool_to_call}, {tool_input})

            tool_response= available_tool[tool_to_call](tool_input)
            print("🔨", {tool_to_call}, {tool_input},{tool_response})

            message_history.append({
                "role":"developer",
                "content":json.dumps({
                    "step":"OBSERVER","tool":tool_to_call,"input":tool_input,"output":tool_response
                })
            })

        elif parsed_result.get("step") == "OUTPUT":
            print("✅", parsed_result.get("content"))
            break

        # gemini want last role to be user
        message_history.append({
            "role": "user",
            "content": "Continue to the next step."
        })

    print("\n")

    

