from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from llm.llm_factory import create_llm_client
from config import Config


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]



graph_builder = StateGraph(State)

# Load configuration
config = Config()

# Create LLM client using the factory with Config object
llm_client = create_llm_client(config)

def chatbot(state: State):
    return {"messages": [llm_client.generate_text(state["messages"], {})]}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


