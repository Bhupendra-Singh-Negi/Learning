from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langgraph.checkpoint.mongodb import MongoDBSaver

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

    
# define graph
graph_builder = StateGraph(State)

# add nodes to builder
graph_builder.add_node("chatbot",chatbot)

# connect edges with nodes and defining flow
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot",END)

# compile the graph
graph=graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return  graph_builder.compile(checkpointer=checkpointer)
    


DB_URI="mongodb://admin:admin@127.0.0.1:27018/?authSource=admin"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer=compile_graph_with_checkpointer(checkpointer=checkpointer)
    thread_config = {
                        "configurable": {
                            "thread_id": "first_thread" # user_id
                            }
                    }
    # # invoke whole output one by one
    # updated_state=graph_with_checkpointer.invoke(
    #     State({"messages":["Hi, whats my name!"]}),
    #     thread_config,
    #     )
    # print("\nUpdated_state",updated_state)

    for chunk in graph_with_checkpointer.stream(
        State({"messages":["+5"]}),
        thread_config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()