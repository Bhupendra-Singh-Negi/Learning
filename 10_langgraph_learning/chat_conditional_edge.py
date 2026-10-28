from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
import os
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good:Optional[bool]

def chatbot(state:State):
    print("\n chatbot response:",state)
    response= client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role":"user","content":state.get("user_query")},
        ]
    )
    state["llm_output"]=response.choices[0].message.content
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini","endnode"]:
    print("\n evaluator response:",state)
    SYSTEM_PROMPT=f"""
        You are an AI response evaluator.

        Compare the user's question with the assistant's answer.

        Return GOOD if the answer is correct and relevant.
        Return BAD if the answer is incorrect or inadequate.

        Return only exact one word "GOOD" or "BAD".
    """
    response=client.chat.completions.create(
        model="openrouter/free",
        messages=[
                    {"role":"system","content":SYSTEM_PROMPT},
                    {"role":"user","content": f"""
                User question: {state["user_query"]}

                Assistant answer: {state["llm_output"]}
                """},
                ]
    )
    state["is_good"]= response.choices[0].message.content.strip().upper() == "GOOD"
         
    if state["is_good"] is True:
        return "endnode"
    else:
        return  "chatbot_gemini"

def chatbot_gemini(state: State):
    print("\n chatbot gemini response:",state)
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role":"System","content":"""
                You are ai assistant and proficient in all field you will answer correctly and accuratly
            """},
            {"role":"user","content":state.get("user_query")},
        ]
    )
    state["llm_output"]=response.choices[0].message.content
    return state

def endnode(state: State):
    print("\n endnode response:",state)
    return state

graph_builder= StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("chatbot_gemini","endnode")
graph_builder.add_edge("endnode", END)

graph= graph_builder.compile()

updatedState=graph.invoke(State({"user_query":"hey what is 2+2"}))
print("\n",updatedState)
