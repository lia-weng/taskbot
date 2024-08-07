import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

from backend.services.reminder import scheduler
from backend.services.llm import invoke_llm
from backend.services.google_service import service_manager

load_dotenv()
app = FastAPI()
middleware_key = os.environ["MIDDLEWARE_KEY"]
app.add_middleware(SessionMiddleware, secret_key=middleware_key)

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
SCOPES = [
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"]

# Serve the static files from the React app's build directory
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/build")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# reminder scheduler
# scheduler.start()

# @app.on_event("shutdown")
# def shutdown_event():
#     if scheduler:
#         scheduler.shutdown()

# authentication
@app.get("/")
async def index():
    with open(os.path.join(frontend_path, "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/check-auth")
async def check_auth(request: Request):
    if "credentials" not in request.session:
        return RedirectResponse(url="/authorize")
    
    stored_creds = request.session["credentials"]
    creds = Credentials(**stored_creds)
    print(creds)
    
    if not creds or creds.expired:
        return RedirectResponse(url="/authorize")

    try:
        print("initializing")
        service_manager.initialize_service(creds)
        oauth2_service = build('oauth2', 'v2', credentials=creds)
        user_info = oauth2_service.userinfo().get().execute()
        email = user_info.get("email")

        response = RedirectResponse(url="/")
        response.set_cookie(key="authenticated", value="true", httponly=False)
        response.set_cookie(key="email", value=email, httponly=False)
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)     


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
    
    return RedirectResponse(url="/check-auth")

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("credentials", None)
    response = RedirectResponse(url="/")
    response.set_cookie(key="authenticated", value="false", httponly=False)
    return response

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


# ngrok http --domain=oyster-ace-sturgeon.ngrok-free.app 8000
