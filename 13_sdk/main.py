from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import os

load_dotenv()
# Configure OpenRouter
client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Configure model
model = OpenAIChatCompletionsModel(
    model="openrouter/free",
    openai_client=client
)

hello_agent = Agent(
    name="Hello world",
    instructions="You are agent which greet user and help in solving user query",
    model=model
)

result = Runner.run_sync(hello_agent, "hey there how are you")

print(result.final_output)
