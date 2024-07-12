import sqlite3
import os
import uuid

from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional

from datetime import datetime, date
import calendar
import dateparser

# Get the path to the database file relative to the current script
db_path = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.db")      

class ToMainAssistant(BaseModel):
    """A tool for routing back to the main assistant."""

@tool
def search_tasks(
    task_name: Optional[str] = None,
    start_date_range: Optional[datetime] = None,
    end_date_range: Optional[datetime] = None,
    status: Optional[str] = None,
    limit: int = 10,
) -> str:
    """Search for tasks based on given criteria."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT * FROM tasks WHERE 1 = 1"
    params = []

    if task_name:
        query += " AND task_name = ?"
        params.append(task_name)
    
    if start_date_range:
        query += " AND due_date >= ?"
        params.append(start_date_range)

    if end_date_range:
        query += " AND due_date <= ?"
        params.append(end_date_range)

    if status is not None:
        query += " AND status = ?"
        params.append(status)

    query += " LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

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

class ToDeleteTasks(BaseModel):
    """Transfers work to a specialized assistant to delete tasks."""

    request: str = Field(
        description="Any information provided by the user."
    )

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

@tool
def get_all_tasks() -> str:
    """Retrive all tasks from the database"""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    
    query = "SELECT * FROM tasks WHERE 1 = 1"
    params = []

    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results

main_tools = [search_tasks, add_tasks, delete_tasks]
delete_tasks_tools = [get_all_tasks, delete_tasks]