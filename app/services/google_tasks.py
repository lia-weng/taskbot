import os.path
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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