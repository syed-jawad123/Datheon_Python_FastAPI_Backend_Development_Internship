import time
from fastapi.testclient import TestClient
from main import app, LOG_FILE

client = TestClient(app)

def test_microservice():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    notif = client.post("/tasks/send-notification", json={
        "recipient_email": "candidate@datheon.in",
        "subject": "Task 4 Evaluation",
        "message": "Async Background worker executed successfully."
    })
    assert notif.status_code == 202
    assert notif.json()["status"] == "queued"

    webhook = client.post("/tasks/dispatch-webhook", json={
        "target_url": "https://api.datheon.in/v1/webhook",
        "event_type": "ORDER_PROCESSED",
        "payload": {"order_id": 9942, "status": "COMPLETED"}
    })
    assert webhook.status_code == 202
    assert webhook.json()["status"] == "queued"

    time.sleep(1.0)
    logs = client.get("/tasks/logs")
    assert logs.status_code == 200

if __name__ == "__main__":
    test_microservice()
    print("ALL TASK 4 MICROSERVICE TESTS PASSED SUCCESSFULLY!")
