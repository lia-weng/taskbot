from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal, Callable
from src.state import State
from src.assistant import Assistant, main_assistant_runnable, delete_tasks_assisant_runnable, BackToMainAssistant
from src.assistant_tools import main_tools, delete_tasks_tools, ToDeleteTasks, get_all_tasks

# def get_all_tasks(state: State):
    # get all tasks
    # let llm decide which one user is deleting
    # returning task_id to delete
    # delete task from db

def route_tasks(state: State):
    route = tools_condition(state)
    if route == "__end__":
        return "__end__"
    
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        if tool_calls[0]["name"] == ToDeleteTasks.__name__:
            return "enter_delete_tasks"
        return route

def route_delete_tasks(state: State):
    route = tools_condition(state)
    if route == "__end__":
        return "__end__"
    
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        if tool_calls[0]["name"] == BackToMainAssistant.__name__:
            return "back_to_main_assistant"
        return "delete_tasks_tools"

def create_entry_node(assistant_name: str) -> Callable:
    def entry_node(state: State) -> dict:
        tool_call_id = state["messages"][-1].tool_calls[0]["id"]
        return {
            "messages": [
                ToolMessage(
                    content=f"The assistant is now the {assistant_name}. Reflect on the above conversation between the main assistant and the user."
                    " Do not mention who you are. Act only as the proxy assistant.",
                    tool_call_id=tool_call_id,
                )
            ]
        }
    
    return entry_node

def back_to_main_assistant(state: State) -> dict:
    return {
        "messages": [
            ToolMessage(
                content="Resuming dialog with the main assistant. Please reflect on the past conversation and assist the user as needed.",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"]
            )
        ]
    }

def create_graph():
    builder = StateGraph(State)

    # main assistant
    builder.add_node("main_assistant", Assistant(main_assistant_runnable))
    builder.add_node("tools", ToolNode(main_tools))
    builder.add_node("back_to_main_assistant", back_to_main_assistant)

    builder.set_entry_point("main_assistant")
    builder.add_conditional_edges("main_assistant", route_tasks)
    builder.add_edge("tools", "main_assistant")
    builder.add_edge("back_to_main_assistant", "main_assistant")

    # delete tasks assistant
    builder.add_node("enter_delete_tasks", create_entry_node("delete task assistant"))
    builder.add_node("delete_tasks_assistant", Assistant(delete_tasks_assisant_runnable))
    builder.add_node("delete_tasks_tools", ToolNode(delete_tasks_tools))

    builder.add_edge("enter_delete_tasks", "delete_tasks_assistant")
    builder.add_conditional_edges("delete_tasks_assistant", route_delete_tasks)
    builder.add_edge("delete_tasks_tools", "delete_tasks_assistant")

    # The checkpointer lets the graph persist its state
    memory = SqliteSaver.from_conn_string(":memory:")
    return builder.compile(checkpointer=memory)
