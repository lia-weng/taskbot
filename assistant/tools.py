import sqlite3
import os
import uuid
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, timedelta
from googleapiclient.discovery import build

from app.services.google_auth import authenticate
from assistant.util import convert_datetime_format


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
    try:
        google_creds = authenticate()
        service = build("tasks", "v1", credentials=google_creds)

        params = {
            "showCompleted": True,
            "showHidden": True
        }

        if status:
            params["showCompleted"] = (status == "completed")

        if start_date:
            params["dueMin"] = convert_datetime_format(start_date)
        if end_date: # dueMax date is not inclusive, so need to add 1 day
            end_date_plus_one_day = end_date + timedelta(days=1)
            params["dueMax"] = convert_datetime_format(end_date_plus_one_day)
        
        print(params["dueMin"], params["dueMax"])

        results = []
        page_token = None

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

    except Exception as e:
        return f"Error: {str(e)}"

def add_task(
    title: str,
    due: datetime,
) -> None:
    """Add a task."""

    try:
        google_creds = authenticate()
        service = build("tasks", "v1", credentials=google_creds)

        task = {
            "title": title,
            "due": due.isoformat() + "Z"
        }

        result = service.tasks().insert(tasklist=TASKLIST_ID, body=task).execute()

        print(f"Added task: {result["id"]}, {result["title"]}, {result["due"]}")
    
    except Exception as e:
        return f"Error: {str(e)}"

# @tool
#TODO def delete_tasks(
#     task_id: str
# ) -> str:
#     """Delete a task given the task_id"""

#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     query = "DELETE FROM tasks WHERE task_id = ?"
#     params = [task_id]
    
#     cursor.execute(query, params)
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return "Task deleted successuflly."


class ToReminderAssistant(BaseModel):
    """Transfers work to a specialized assistant to send reminders."""

    request: str = Field(
        description="Any information provided by the user."
    )


main_tools = [search_tasks, add_task]
# main_tools = [search_tasks, add_tasks, delete_tasks, ToReminderAssistant]
reminder_tools = [search_tasks, ToMainAssistant]