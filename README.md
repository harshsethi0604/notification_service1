# Notification Service API 🚀

This is a FastAPI-based notification system that sends notifications via:
- 📧 Email (using SMTP)
- 📱 SMS (via Twilio)
- 💬 In-app (stored locally)

## Features
- Asynchronous email sending with `aiosmtplib`
- SMS notifications using Twilio
- In-app notifications stored in memory
- Background task queue using Redis + RQ
- Retry mechanism for failed jobs

## API Endpoints
- `POST /notifications` → Send a notification
- `GET /users/{user_id}/notifications` → View user's notifications

## Technologies Used
- Python
- FastAPI
- Redis + RQ
- Twilio API
- Gmail SMTP

## Setup Instructions
1. Clone the repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
3. Add your environment variables to a .env file (see .env.example)

4. Run FastAPI:uvicorn main:app --reload
5.Start the worker:rq worker

