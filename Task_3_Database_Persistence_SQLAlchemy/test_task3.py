from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_sql_persistence():
    u_resp = client.post("/users", json={"username": "jawad_ai", "email": "jawad@biit.edu.pk"})
    assert u_resp.status_code in (201, 400)
    user_id = u_resp.json()["id"] if u_resp.status_code == 201 else 1

    note_resp = client.post(f"/users/{user_id}/notes", json={
        "title": "FastAPI + SQLAlchemy Architecture",
        "content": "Implemented clean declarative relational models with foreign keys.",
        "is_archived": False
    })
    assert note_resp.status_code == 201
    assert note_resp.json()["user_id"] == user_id

    user_detail = client.get(f"/users/{user_id}")
    assert user_detail.status_code == 200
    assert len(user_detail.json()["notes"]) >= 1

if __name__ == "__main__":
    test_sql_persistence()
    print("ALL TASK 3 SQLALCHEMY TESTS PASSED SUCCESSFULLY!")
