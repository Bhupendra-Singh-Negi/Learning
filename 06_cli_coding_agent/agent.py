from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import requests

load_dotenv()
BASE_DIR=Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH=BASE_DIR/"system_prompt.txt"

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

client = OpenAI(
   base_url="https://integrate.api.nvidia.com/v1",
  api_key=os.getenv("OPENROUTER_API_KEY")
)
def write_file(path: str, content: str):
    """Create or update a file inside the agent's working directory."""
    try:
        target_path = (BASE_DIR / path).resolve()

        # Prevent writing outside the project directory
        target_path.relative_to(BASE_DIR.resolve())

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")

        return f"Successfully wrote {target_path.relative_to(BASE_DIR)}"

    except ValueError:
        return "Error: File path must stay inside the project directory."
    except OSError as e:
        return f"Error writing file: {e}"
    
def run_command(cmd:str):
    result= os.system(cmd)
    return result

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response=requests.get(url)

    if response.status_code==200:
        return f"The weather in {city} is {response.text}"

    return "Sorry, Something went wrong"

available_tool={
    "get_weather":get_weather,
    "run_command":run_command,
    "write_file": write_file,
    }


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
            extra_body={
                "models": [
                    "recursive/flint-v1.0:free",
                    "minimax/minimax-m3.1-flash:free",
                    "google/gemma-4-26b-a4b-it:free",
                ]
            },
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

        elif parsed_result.get("step") == "TOOL":
            tool_to_call = parsed_result.get("tool")
            tool_input = parsed_result.get("input")

            print("🔨", tool_to_call, tool_input)

            if tool_to_call == "write_file":
                # Handle input returned as a JSON string
                if isinstance(tool_input, str):
                    try:
                        tool_input = json.loads(tool_input)
                    except json.JSONDecodeError:
                        tool_response = (
                            "Error: write_file input must be a JSON object "
                            'containing "path" and "content".'
                        )
                        tool_input = None

                if isinstance(tool_input, dict):
                    path = tool_input.get("path")
                    content = tool_input.get("content")

                    if isinstance(path, str) and isinstance(content, str):
                        tool_response = write_file(path, content)
                    else:
                        tool_response = (
                            'Error: write_file requires string fields "path" '
                            'and "content".'
                        )
                elif tool_input is not None:
                    tool_response = "Error: Invalid write_file input."

            elif tool_to_call in available_tool:
                if isinstance(tool_input, str):
                    tool_response = available_tool[tool_to_call](tool_input)
                else:
                    tool_response = "Error: This tool expects a string input."

            else:
                tool_response = f"Error: Unknown tool '{tool_to_call}'."

            print("🔨", tool_to_call, tool_response)

            message_history.append({
                "role": "developer",
                "content": json.dumps({
                    "step": "OBSERVER",
                    "tool": tool_to_call,
                    "input": tool_input,
                    "output": tool_response
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

    

