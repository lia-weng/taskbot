from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class ServiceManager:
    def __init__(self):
        self._service = None
        self._tasklist_id = None

    def initialize_service(self, credentials):
        try:
            self._service = build("tasks", "v1", credentials=credentials)
            self._initialize_tasklist()
        except Exception as e:
            print(f"Error initializing service: {e}")
        return self._service

    def _initialize_tasklist(self):
        try:
            # Check if "taskbot" task list exists
            tasklists = self._service.tasklists().list().execute()
            print("initializing tasklist")
            for tasklist in tasklists.get("items", []):
                if tasklist["title"] == "taskbot":
                    self._tasklist_id = tasklist["id"]
                    print("has taskbot")
                    break
                else:
                    # Create "taskbot" task list if it doesn't exist
                    tasklist = {
                        "title": "taskbot"
                    }
                    created_tasklist = self._service.tasklists().insert(body=tasklist).execute()
                    self._tasklist_id = created_tasklist["id"]
                    print("no taskbot")
        except Exception as e:
            print(f"Error initializing task list: {e}")

    @property
    def service(self):
        return self._service

    @property
    def tasklist_id(self):
        return self._tasklist_id

service_manager = ServiceManager()

