from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)   

# defining state
class State(TypedDict):
    messages:Annotated[list, add_messages]

# defining nodes
def chatbot(state: State):
    response=llm.invoke(state.get("messages"))
    print("\n")
    return {"messages": [response]}

def sample(state:State):
    # response=llm.invoke(state.get("messages"))
    print("\nInside sample node",state)
    return {"messages": ["sample message Node"]}
    
# define graph
graph_builder = StateGraph(State)

# add nodes to builder
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sample",sample)

# connect edges with nodes and defining flow
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot","sample")
graph_builder.add_edge("sample",END)

# compile the graph
graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":["Hi, how are you!"]}))
print("\nUpdated_state",updated_state)

