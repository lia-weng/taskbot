import os
import sqlite3
import schedule
import time
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from src.util import llm

db_path = os.path.join(os.path.dirname(__file__), "data", "tasks.db") 

def get_all_tasks() -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT * FROM tasks"

    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results

tasks = get_all_tasks()


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a task reminder assistant."
            " Your primary role is remind user of their upcoming tasks."
            " The user has the following tasks: {tasks}"
            f" The time right now is {datetime.now()}."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())
reminder_assistant_runnable = prompt | llm

def send_reminder():
    print(time.time())
    reminder = reminder_assistant_runnable.invoke({"tasks": tasks})
    reminder.pretty_print()

schedule.every(3).seconds.do(send_reminder)

start_time = time.time()

while time.time() - start_time < 9:
    schedule.run_pending()