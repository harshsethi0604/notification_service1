import asyncio
from notifiers import send_email, send_sms

def send_notification_task(user_id: str, notif_type: str, message: str):
    try:
        if notif_type == "email":
            asyncio.run(send_email(user_id, message))
        elif notif_type == "sms":
            send_sms(user_id, message)
        else:
            raise ValueError(f"Unknown notification type: {notif_type}")
    except Exception as e:
        print(f"Error sending {notif_type} notification to {user_id}: {e}")
        raise  # Re-raise the exception to trigger retry in RQ
