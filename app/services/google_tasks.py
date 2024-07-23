import os.path
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import Optional, Literal
from datetime import datetime


load_dotenv()
TASKLIST_ID = os.getenv("TASKLIST_ID")

def get_tasklists(creds):
    service = build("tasks", "v1", credentials=creds)

    try:
      results = service.tasklists().list(maxResults=10).execute()
      tasklists = results.get("items", [])
    except HttpError as err:
      print("Cannot retrieve tasklists" + err)

    if not tasklists:
        print("No task lists found.")
        return None

    print("Task lists:")
    for tasklist in tasklists:
        print(f"{tasklist["id"]} {tasklist["title"]}")
    
    return tasklist

def get_tasks(creds):
    service = build("tasks", "v1", credentials=creds)

    try:
      results = service.tasks().list(tasklist=TASKLIST_ID).execute()
      tasks = results.get("items", [])
    except HttpError as err:
      print("Cannot retrieve tasks" + err)

    if not tasks:
        print("No tasks found.")
        return None
    
    print("Tasks:")
    for task in tasks:
       print(f"{task["id"]} {task["title"]} {task["due"]}")
    
    return tasks

def search_tasks(
      creds,
      title: Optional[str] = None,
      status: Optional[Literal["needsAction", "completed"]] = None,
      start_date: Optional[datetime] = None,
      end_date: Optional[datetime] = None,
      max_results: int = 20
) -> list:
  service = build("tasks", "v1", credentials=creds)

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