import os
import sqlite3
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import tools_condition, ToolNode

from src.util import llm, builder, Assistant, create_entry_node, create_sub_assistant_routes, State
from src.tools import reminder_tools, ToMainAssistant


reminder_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized task reminder assistant."
            " You should act as the user's friend and ask them if they have completed the task."
            f" The time right now is {datetime.now()}."
            # " If the user has an upcoming task within the next three days, send reminder."
            # " If not, don't send anything."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

reminder_assistant_runnable = reminder_assistant_prompt | llm.bind_tools(
    reminder_tools
)

def reminder_assistant_routes(state: State):
    route = tools_condition(state)
    if route == "__end__":
        return "__end__"
    
    tool_calls = state["messages"][-1].tool_calls
    action_complete = any(tc["name"] == ToMainAssistant.__name__ for tc in tool_calls)
    if action_complete:
        return "to_main_assistant"
    return "reminder_tools"

def create_reminder_assistant():
    builder.add_node("enter_reminder_assistant", create_entry_node("reminder assistant"))
    builder.add_node("reminder_assistant", Assistant(reminder_assistant_runnable))
    builder.add_node("reminder_tools", ToolNode(reminder_tools))

    builder.add_edge("enter_reminder_assistant", "reminder_assistant")
    builder.add_conditional_edges("reminder_assistant", reminder_assistant_routes)
    builder.add_edge("reminder_tools", "reminder_assistant")