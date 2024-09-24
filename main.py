from fastapi import FastAPI
import asyncio
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

app = FastAPI()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

load_dotenv()
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

TIMER_DURATION = 600
timer_task = None

async def send_email():
    msg = MIMEText("10-minute timer has expired, something is probably wrong")
    msg["Subject"] = "Raspberry Pi Timer Notification"
    msg["From"] = SMTP_USERNAME
    msg["To"] = RECIPIENT_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

async def timer():
    await asyncio.sleep(TIMER_DURATION)
    await send_email()

@app.on_event("startup")
async def start_timer():
    global timer_task
    timer_task = asyncio.create_task(timer())
    print("Timer started.")

@app.post("/reset-timer")
async def reset_timer():
    global timer_task
    if timer_task:
        timer_task.cancel()
        print("Timer canceled")
    timer_task = asyncio.create_task(timer())
    print("Timer reset and started again")
    return {"message": "Timer reset and started again"}
