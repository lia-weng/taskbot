from dotenv import load_dotenv
from typing import Annotated, Callable, Literal
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import tools_condition

from src.tools import ToMainAssistant

load_dotenv()

class Task(TypedDict):
    task_id: int
    task_name: str
    due_date: str
    status: Literal['done', 'not started', 'in progress']

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_tasks: list[Task]

llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
)

builder = StateGraph(State)

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

def create_entry_node(assistant_name: str) -> Callable:
    def entry_node(state: State) -> dict:
        tool_call_id = state["messages"][-1].tool_calls[0]["id"]
        return {
            "messages": [
                ToolMessage(
                    content=f"The assistant is now the {assistant_name}. Reflect on the above conversation between the main assistant and the user.",
                    # " Do not mention who you are. Act only as the proxy assistant.",
                    tool_call_id=tool_call_id,
                )
            ]
        }
    
    return entry_node


def create_sub_assistant_routes(tool_name: str):
    def route(state: State):
        route = tools_condition(state)
        print("route", route)
        if route == "__end__":
            return "__end__"
        
        tool_calls = state["messages"][-1].tool_calls
        action_complete = any(tc["name"] == ToMainAssistant.__name__ for tc in tool_calls)
        if action_complete:
            return "to_main_assistant"
        return tool_name
    
    return route