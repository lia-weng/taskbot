import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

from app.services.reminder import scheduler
from app.services.llm import invoke_llm
from app.services.google_service import service_manager

load_dotenv()
app = FastAPI()
middleware_key = os.environ["MIDDLEWARE_KEY"]
app.add_middleware(SessionMiddleware, secret_key=middleware_key)

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
SCOPES = ["https://www.googleapis.com/auth/tasks"]

# reminder scheduler
# scheduler.start()

# @app.on_event("shutdown")
# def shutdown_event():
#     if scheduler:
#         scheduler.shutdown()

# authentication
@app.get("/")
async def index(request: Request):
    if "credentials" not in request.session:
        return RedirectResponse(url="/authorize")

    creds = Credentials(**request.session["credentials"])
    service_manager.initialize_service(creds)

    return JSONResponse(content={"message": "Authorized!"})

@app.get("/authorize")
async def authorize(request: Request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )
    flow.redirect_uri = request.url_for("oauth2callback")

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )

    request.session["state"] = state
    return RedirectResponse(url=authorization_url)

@app.get("/oauth2callback")
async def oauth2callback(request: Request):
    state = request.session.get("state")
    if not state:
        raise HTTPException(status_code=400, detail="State missing from session.")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = request.url_for("oauth2callback")

    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials
    request.session["credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    }

    return RedirectResponse(url="/")

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("credentials", None)
    return RedirectResponse(url="/")

#twilio
@app.post("/sms")
async def handle_sms(request: Request):
    try:
        form_data = await request.form()
        user_message = form_data.get("Body", None).strip()
        ai_message = invoke_llm(user_message)

        resp = MessagingResponse()
        resp.message(ai_message)
        
        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return Response(content="An error occurred", status_code=500)


# ngrok http --domain=oyster-ace-sturgeon.ngrok-free.app 5000
