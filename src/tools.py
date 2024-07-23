import sqlite3
import os
import uuid
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import dateutil.parser
from googleapiclient.discovery import build

from app.services.google_auth import authenticate

db_path = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.db")

google_creds = authenticate()

load_dotenv()
TASKLIST_ID = os.getenv("TASKLIST_ID")


class ToMainAssistant(BaseModel):
    """A tool for routing back to the main assistant."""

@tool
def search_tasks(
    title: Optional[str] = None,
    status: Optional[Literal["needsAction", "completed"]] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    max_results: Optional[int] = 20
) -> str:
    """Retrieve tasks based on search criteria."""
    
    service = build("tasks", "v1", credentials=google_creds)

    params = {
        "showCompleted": True,
        "showHidden": True
    }

    if status:
        params["showCompleted"] = (status == "completed")

    if start_date:
        params["dueMin"] = start_date.isoformat() + "Z"
    if end_date:
        params["dueMax"] = end_date.isoformat() + "Z"

    results = []

    while True:
        if page_token:
            params["pageToken"] = page_token

            tasks = service.tasks().list(tasklist=TASKLIST_ID, **params).execute()

            for task in tasks.get("items", []):
                if title:
                    if title.lower() in task.get("title", "").lower():
                        results.append(task)
                else:
                    results.append(task)

        page_token = tasks.get("nextPageToken")
        if not page_token or len(results) >= max_results:
            break

    return results

@tool
def add_tasks(
    task_name: str,
    due_date: datetime,
    status: Optional[str] = None,
) -> None:
    "Add a task. If user didn't mention a specific time, default to T00:00:00 of that day."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    task_id = str(uuid.uuid4())
    if not status:
        status = "not started"

    query = """
    INSERT INTO tasks (task_id, task_name, due_date, status)
    VALUES (?, ?, ?, ?)
    """
    params = [
        task_id,
        task_name,
        due_date.strftime('%Y-%m-%d %H:%M:%S'),
        status
    ]
    
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

    return "Task added successuflly."

@tool
def delete_tasks(
    task_id: str
) -> str:
    """Delete a task given the task_id"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "DELETE FROM tasks WHERE task_id = ?"
    params = [task_id]
    
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

    return "Task deleted successuflly."


class ToReminderAssistant(BaseModel):
    """Transfers work to a specialized assistant to send reminders."""

    request: str = Field(
        description="Any information provided by the user."
    )


main_tools = [search_tasks, add_tasks, delete_tasks, ToReminderAssistant]
reminder_tools = [search_tasks, ToMainAssistant]