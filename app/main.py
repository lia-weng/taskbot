import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from langchain_core.messages import HumanMessage
from twilio.twiml.messaging_response import MessagingResponse

from assistant.schedule_reminder import scheduler
from assistant.graph import create_graph

load_dotenv()
app = FastAPI()

graph = create_graph()
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        "thread_id": thread_id,
    }
}

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
        # Get the message the user sent our Twilio number
        form_data = await request.form()
        user_message = form_data.get('Body', None).strip()

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=user_message)
                ]
            },
            config
        )

        ai_message = result["messages"][-1].content

        if ai_message == "no_tasks":
            return None

        # Create Twilio response
        resp = MessagingResponse()
        resp.message(ai_message)
        
        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return Response(content="An error occurred", status_code=500)


# ngrok http --domain=oyster-ace-sturgeon.ngrok-free.app 5000
