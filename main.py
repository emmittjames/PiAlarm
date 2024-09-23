from fastapi import FastAPI, BackgroundTasks
import asyncio
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"  # Replace with your email
SMTP_PASSWORD = "your-password"        # Replace with your email password or app-specific password
RECIPIENT_EMAIL = "emmittjames1@gmail.com"  # Replace with the recipient"s email

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
