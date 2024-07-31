from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class ServiceManager:
    def __init__(self):
        self._service = None
        self._tasklist_id = None

    def initialize_service(self, credentials):
        if self._service is None:
            self._service = build("tasks", "v1", credentials=credentials)
            self._initialize_tasklist()
        return self._service

    def _initialize_tasklist(self):
        # Check if "taskbot" task list exists
        tasklists = self._service.tasklists().list().execute()
        for tasklist in tasklists.get("items", []):
            if tasklist["title"] == "taskbot":
                self._tasklist_id = tasklist["id"]
                break
        else:
            # Create "taskbot" task list if it doesn't exist
            tasklist = {
                "title": "taskbot"
            }
            created_tasklist = self._service.tasklists().insert(body=tasklist).execute()
            self._tasklist_id = created_tasklist["id"]

    @property
    def service(self):
        return self._service

    @property
    def tasklist_id(self):
        return self._tasklist_id

service_manager = ServiceManager()

