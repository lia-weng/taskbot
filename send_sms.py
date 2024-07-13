import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
messaging_service_sid = os.environ["TWILIO_MESSAGING_SID"]
client = Client(account_sid, auth_token)

# message = client.messages.create(
#     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#     from_="+15015312621",
#     to="+14164586922",
# )

# print(message.body)

message = client.messages.create(
    messaging_service_sid=messaging_service_sid,
    to="+14164586922",
    body="This will be the body of the new message!",
)

print(message.body)