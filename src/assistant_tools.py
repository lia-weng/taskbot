import sqlite3
import os

from langchain_core.tools import tool
from typing import Optional

from datetime import datetime, date
import calendar
import dateparser

# Get the path to the database file relative to the current script
db_path = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.db")      

@tool
def search_tasks(
    task_name: Optional[str] = None,
    start_date_range: Optional[datetime] = None,
    end_date_range: Optional[datetime] = None,
    status: Optional[str] = None,
    limit: int = 10,
) -> list[dict]:
    """Search for tasks based on given crSiteria."""
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

tools = [search_tasks]