from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal
from src.state import State
from src.assistant import Assistant, main_assistant_runnable
from src.assistant_tools import tools


def create_graph():
    builder = StateGraph(State)

    builder.add_node("main_assistant", Assistant(main_assistant_runnable))
    builder.add_node("tools", ToolNode(tools))
    builder.set_entry_point("main_assistant")
    builder.add_conditional_edges("main_assistant", tools_condition)
    builder.add_edge("tools", "main_assistant")

    # The checkpointer lets the graph persist its state
    memory = SqliteSaver.from_conn_string(":memory:")
    return builder.compile(checkpointer=memory)
