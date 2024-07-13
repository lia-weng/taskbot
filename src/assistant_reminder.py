import os
import sqlite3
import schedule
import time
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import tools_condition, ToolNode

from src.util import llm, builder, Assistant, create_entry_node, create_sub_assistant_routes
from src.tools import reminder_tools


reminder_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized task reminder assistant."
            " You should act as the user's friend and ask them if they have completed the task."
            f" The time right now is {datetime.now()}."
            " If the user has an upcoming task within the next three days, send reminder."
            " If not, don't send anything."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

reminder_assistant_runnable = reminder_assistant_prompt | llm.bind_tools(
    reminder_tools
)

def create_reminder_assistant():
    builder.add_node("enter_reminder_assistant", create_entry_node("reminder assistant"))
    builder.add_node("reminder_assistant", Assistant(reminder_assistant_runnable))
    builder.add_node("reminder_tools", ToolNode(reminder_tools))

    builder.add_edge("enter_reminder_assistant", "reminder_assistant")
    builder.add_conditional_edges("reminder_assistant", create_sub_assistant_routes("reminder_tools"))
    builder.add_edge("reminder_tools", "reminder_assistant")

# def send_reminder():
#     print(time.time())
#     reminder = reminder_assistant_runnable.invoke({"tasks": tasks})
#     reminder.pretty_print()

# schedule.every(3).seconds.do(send_reminder)

# start_time = time.time()

# while time.time() - start_time < 9:
#     schedule.run_pending()