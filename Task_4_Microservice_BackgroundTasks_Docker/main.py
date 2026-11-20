"""
Datheon Python + FastAPI Backend Development Internship
Task 4: Microservice with Background Tasks & Docker
Application ID: DT-2026-89H4F | Candidate: Syed Jawad Hussain Shah
"""

import time
import os
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, status
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="Datheon Microservice: BackgroundTasks & Rate Limiting",
    description="Containerized microservice architecture with async task dispatchers, health monitoring, and rate limiting.",
    version="1.0.0"
)

LOG_FILE = "background_events.log"

RATE_LIMIT_MAX = 20
RATE_LIMIT_WINDOW = 10
request_history = defaultdict(list)

def rate_limit_check(client_ip: str):
    now = time.time()
    request_history[client_ip] = [t for t in request_history[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(request_history[client_ip]) >= RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait a few seconds before retrying."
        )
    request_history[client_ip].append(now)

def async_email_worker(recipient: str, subject: str, message: str):
    time.sleep(0.5)
    log_entry = f"[{datetime.now(timezone.utc).isoformat()}] [EMAIL_DISPATCH] To: {recipient} | Subject: {subject} | Body: {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

def async_webhook_worker(target_url: str, event_type: str, payload: dict):
    time.sleep(0.3)
    log_entry = f"[{datetime.now(timezone.utc).isoformat()}] [WEBHOOK_DISPATCH] URL: {target_url} | Event: {event_type} | Payload: {payload}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

class NotificationRequest(BaseModel):
    recipient_email: EmailStr
    subject: str
    message: str

class WebhookRequest(BaseModel):
    target_url: str
    event_type: str
    payload: dict

@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    rate_limit_check(client_ip)
    response = await call_next(request)
    return response

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "datheon-microservice",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "docker_containerized": True,
        "app_id": "DT-2026-89H4F"
    }

@app.post("/tasks/send-notification", status_code=status.HTTP_202_ACCEPTED, tags=["Background Tasks"])
def trigger_notification(payload: NotificationRequest, bg: BackgroundTasks):
    bg.add_task(async_email_worker, payload.recipient_email, payload.subject, payload.message)
    return {
        "status": "queued",
        "message": f"Async email task queued for {payload.recipient_email}",
        "queued_at": datetime.now(timezone.utc).isoformat()
    }

@app.post("/tasks/dispatch-webhook", status_code=status.HTTP_202_ACCEPTED, tags=["Background Tasks"])
def trigger_webhook(payload: WebhookRequest, bg: BackgroundTasks):
    bg.add_task(async_webhook_worker, payload.target_url, payload.event_type, payload.payload)
    return {
        "status": "queued",
        "message": f"Async webhook dispatched for {payload.event_type}",
        "queued_at": datetime.now(timezone.utc).isoformat()
    }

@app.get("/tasks/logs", tags=["Background Tasks"])
def read_task_logs():
    if not os.path.exists(LOG_FILE):
        return {"logs": []}
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return {"logs": [line.strip() for line in lines[-20:]]}
