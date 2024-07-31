from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class ServiceManager:
    def __init__(self):
        self._service = None

    def initialize_service(self, credentials):
        if self._service is None:
            self._service = build("tasks", "v1", credentials=credentials)
        return self._service

service_manager = ServiceManager()

