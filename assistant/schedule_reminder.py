import httpx
import asyncio
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta

async def call_sms_route():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/sms", data={"Body": "Automated: Send reminder for today's task."})
            print(response.text)
    except Exception as e:
        print(f"Error calling /sms route: {e}")

def send_reminder():
    asyncio.run(call_sms_route())
    schedule_next_reminder()


def schedule_next_reminder():
    delay_seconds = random.randint(5, 20)
    next_run_time = datetime.now() + timedelta(seconds=delay_seconds)
    scheduler.add_job(send_reminder, DateTrigger(run_date=next_run_time))
    print(f"Next reminder scheduled at {next_run_time}")

scheduler = BackgroundScheduler()
# scheduler.add_job(send_reminder, DateTrigger(run_date=datetime.now().replace(hour=2, minute=21, second=0, microsecond=0)))

initial_run_time = datetime.now() + timedelta(seconds=3)
scheduler.add_job(send_reminder, DateTrigger(run_date=initial_run_time))