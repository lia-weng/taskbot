import sqlite3
import os
import uuid
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, timedelta
from googleapiclient.discovery import build

from app.services.google_auth import get_service
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
        service = get_service()

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

@tool
def add_task(
    title: str,
    due: datetime,
) -> None:
    """Add a task."""

    try:
        service = get_service()

        task = {
            "title": title,
            "due": convert_datetime_format(due)
        }

        result = service.tasks().insert(tasklist=TASKLIST_ID, body=task).execute()

        print(f"Added task: {result["id"]}, {result["title"]}, {result["due"]}")
    
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def delete_task(
    task_id: str
) -> None:
    """Delete tasks based on task ID."""
    try:
        service = get_service()
        service.tasks().delete(tasklist=TASKLIST_ID, task=task_id).execute()
    
    except Exception as e:
        return f"Error: {str(e)}"


class ToReminderAssistant(BaseModel):
    """Transfers work to a specialized assistant to send reminders."""

    request: str = Field(
        description="Any information provided by the user."
    )


main_tools = [search_tasks, add_task, delete_task]
reminder_tools = [search_tasks, ToMainAssistant]