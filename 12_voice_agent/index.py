import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os
import asyncio

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)
async_client=AsyncOpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
      model="fish-audio/s2.1-pro-free:free",
        voice="b347db033a6549378b48d00acb0d06cd",
        input=speech,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold=2

        SYSTEM_PROMPT="""
            You're an expert voice agent.
            You will transcript of what user has said using voice.
            You need to give output as if you are giving answer in voice agent and whatever you speek will be converted back to audio using ai and played backed to user.
        """

        messages =[{"role":"system","content":SYSTEM_PROMPT}]

        while True:
            print("\nSpeak Something...")
            audio = r.listen(source)

            print("\nProcessing Audio...(STT)")
            stt=r.recognize_google(audio)

            print("\nYou said:", stt)

            messages.append({"role":"user","content":stt})
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages
            )
            print("AI response:", response.choices[0].message.content)

            asyncio.run(tts(speech=response.choices[0].message.content))


main()