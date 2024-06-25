import os

from langchain.agents import AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.globals import set_debug
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

set_debug(True)

_ = load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Alfa"

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tools = [DuckDuckGoSearchRun()]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are helpful AI assistant. Only of you don't know answer use tool for search",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind_tools(tools)

agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def get_response(input_text: str) -> str:
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful AI assistant, if you don't know the answer to {question}, return I don't know.")
    chain = prompt | llm
    chain_response = chain.invoke({"question": input_text})
    output = chain_response.content

    if "I don't know" in output or "I'm not sure" in output:
        agent_response = agent_executor.invoke({"input": input_text})
        output = agent_response["output"]
    return output


# Example usage
input_text = "What is the weather in Paris today?"
response = get_response(input_text)
print(response)
