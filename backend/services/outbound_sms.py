import httpx
import asyncio
import os
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from twilio.rest import Client

from backend.services.llm import invoke_llm
from backend.services.service_manager import service_manager

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
phone_number_from = os.environ["PHONE_NUMBER_FROM"]
phone_number_to = os.environ["PHONE_NUMBER_TO"]

twilio_client = Client(account_sid, auth_token)

def send_welcome():
    # twilio_client.messages.create(
    #     body="Hi, this is Taskbot 👋",
    #     from_=phone_number_from,
    #     to=service_manager.phone_number,
    # )
    print("welcome")

def send_reminder():
    ai_message = invoke_llm("Automated: Send reminder for today's task.")
    print(ai_message)

    print(service_manager.phone_number)

    if ai_message != "no_tasks":
        twilio_client.messages.create(
            body=ai_message,
            from_=phone_number_from,
            to=service_manager.phone_number,
        )

    # schedule_next_reminder()


def schedule_next_reminder():
    delay_seconds = random.randint(5, 20)
    next_run_time = datetime.now() + timedelta(seconds=delay_seconds)
    scheduler.add_job(send_reminder, DateTrigger(run_date=next_run_time))
    print(f"Next reminder scheduled at {next_run_time}")

scheduler = BackgroundScheduler()
# scheduler.add_job(send_reminder, DateTrigger(run_date=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)))