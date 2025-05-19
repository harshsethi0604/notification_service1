import os
from dotenv import load_dotenv
import aiosmtplib
from email.message import EmailMessage
from twilio.rest import Client

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")


async def send_email(to_email: str, message: str):
    email = EmailMessage()
    email["From"] = EMAIL_USERNAME
    email["To"] = to_email
    email["Subject"] = "Notification"
    email.set_content(message)

    await aiosmtplib.send(
        email,
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        start_tls=True,
        username=EMAIL_USERNAME,
        password=EMAIL_PASSWORD,
    )


def send_sms(to_number: str, message: str):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=to_number
    )
