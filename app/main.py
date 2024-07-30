from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

from app.services.reminder import scheduler
from app.services.llm import invoke_llm

load_dotenv()
app = FastAPI()

scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    if scheduler:
        scheduler.shutdown()


# routes
@app.get("/")
async def main_route():
    return PlainTextResponse("taskbot")


@app.post("/sms")
async def handle_sms(request: Request):
    try:
        form_data = await request.form()
        user_message = form_data.get('Body', None).strip()
        ai_message = invoke_llm(user_message)

        resp = MessagingResponse()
        resp.message(ai_message)
        
        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return Response(content="An error occurred", status_code=500)


# ngrok http --domain=oyster-ace-sturgeon.ngrok-free.app 5000
