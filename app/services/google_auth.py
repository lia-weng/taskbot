import os
import json
import logging
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/tasks']

def authenticate():
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    # logger.debug(f"Token file exists: {os.path.exists(token_path)}")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # logger.debug(f"Token file permissions: {oct(os.stat(token_path).st_mode)[-3:]}")
        with open(token_path, 'r') as token_file:
            token_content = json.load(token_file)
            # logger.debug(f"Token contains refresh_token: {'refresh_token' in token_content}")

    if not creds or not creds.valid:
        # logger.debug(f"Credentials valid: {creds.valid if creds else 'No creds'}")
        # logger.debug(f"Credentials expired: {creds.expired if creds else 'No creds'}")
        # logger.debug(f"Refresh token exists: {bool(creds.refresh_token) if creds else 'No creds'}")

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')

        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    return creds