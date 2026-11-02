from dotenv import load_dotenv
import os
import json
from pathlib import Path
from pydantic import BaseModel, Field
import requests
from typing import Optional
import json

import speech_recognition as sr
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio

load_dotenv()

async_client=AsyncOpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

client = OpenAI(
   base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY")
)

async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
      model="fish-audio/s2.1-pro-free:free",
        voice="b347db033a6549378b48d00acb0d06cd",
        input=speech,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

# def write_file(path: str, content: str):
#     """Create or update a file inside the agent's working directory."""
#     try:
#         target_path = (BASE_DIR / path).resolve()

#         # Prevent writing outside the project directory
#         target_path.relative_to(BASE_DIR.resolve())

#         target_path.parent.mkdir(parents=True, exist_ok=True)
#         target_path.write_text(content, encoding="utf-8")

#         return f"Successfully wrote {target_path.relative_to(BASE_DIR)}"

#     except ValueError:
#         return "Error: File path must stay inside the project directory."
#     except OSError as e:
#         return f"Error writing file: {e}"
    
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
    # "write_file": write_file,
    }
BASE_DIR=Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH=BASE_DIR/"system_prompt.txt"

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")
    
print("\n")
message_history = [
    {"role":"system","content":SYSTEM_PROMPT},
]

def main():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold=2

        while True:

            print("\nSpeak Something...")
            audio = r.listen(source)

            print("\nProcessing Audio...(STT)")
            stt=r.recognize_google(audio)

            print("\nYou said:", stt)

            message_history.append({"role":"user","content":stt})

            while True:
                response = client.chat.completions.parse(
                    model="nvidia/nemotron-3.5-super-vl:free",
                    response_format=MyOutputFormat,
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
                    asyncio.run(tts(speech=parsed_result.get("content")))
                    break

                # gemini want last role to be user
                message_history.append({
                    "role": "user",
                    "content": "Continue to the next step."
                })

            print("\n")

if __name__ == "__main__":
    asyncio.run(main())
