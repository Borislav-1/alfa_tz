import os
from langgraph.prebuilt import ToolNode
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.globals import set_debug
import operator
from typing import Annotated, Sequence, TypedDict
from langgraph.graph import END, StateGraph

from langchain_core.messages import BaseMessage

set_debug(True)

_ = load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Alfa"

tools = [DuckDuckGoSearchRun()]
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
model = model.bind_tools(tools)

tool_node = ToolNode(tools)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


def call_model(state):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

workflow.add_edge("action", "agent")
app = workflow.compile()

# Example usage
inputs = {"messages": [HumanMessage(content="What is the weather in Paris today?")]}
response = app.invoke(inputs)
content = response["messages"][-1].content
print(content)
