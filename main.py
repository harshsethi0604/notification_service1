from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uuid
from redis import Redis
from rq import Queue, Retry
from tasks import send_notification_task

app = FastAPI()

# In-memory store for in-app notifications
notifications_db = {}

# Redis connection and RQ queue
redis_conn = Redis()
task_queue = Queue(connection=redis_conn)

# Models
class NotificationRequest(BaseModel):
    user_id: str
    type: str  # "email", "sms", or "in-app"
    message: str

class Notification(BaseModel):
    id: str
    user_id: str
    type: str
    message: str

# API endpoint to send a notification
@app.post("/notifications")
async def send_notification(notification: NotificationRequest):
    notif_id = str(uuid.uuid4())
    new_notif = Notification(
        id=notif_id,
        user_id=notification.user_id,
        type=notification.type,
        message=notification.message
    )
    notifications_db.setdefault(notification.user_id, []).append(new_notif)

    try:
        if notification.type in ["email", "sms"]:
            # Enqueue the background task with retry logic
            task_queue.enqueue(
                send_notification_task,
                notification.user_id,
                notification.type,
                notification.message,
                retry=Retry(max=3, interval=[10, 30, 60])  # Retry 3 times with delays in seconds
            )
        # In-app notifications are already stored above
    except Exception as e:
        return {"status": "failed", "error": str(e)}

    return {"status": "queued", "id": notif_id}

# API endpoint to get user notifications
@app.get("/users/{user_id}/notifications", response_model=List[Notification])
def get_user_notifications(user_id: str):
    return notifications_db.get(user_id, [])
