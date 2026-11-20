from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_auth_workflow():
    reg_user = client.post("/auth/register", json={
        "username": "student_dev",
        "email": "student@datheon.in",
        "password": "Password123!",
        "role": "user"
    })
    assert reg_user.status_code == 201
    
    reg_admin = client.post("/auth/register", json={
        "username": "lead_architect",
        "email": "lead@datheon.in",
        "password": "AdminSecret456!",
        "role": "admin"
    })
    assert reg_admin.status_code == 201

    login_user = client.post("/auth/login", data={"username": "student_dev", "password": "Password123!"})
    assert login_user.status_code == 200
    user_token = login_user.json()["access_token"]

    me_resp = client.get("/users/me", headers={"Authorization": f"Bearer {user_token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "student_dev"

    admin_fail = client.get("/admin/dashboard", headers={"Authorization": f"Bearer {user_token}"})
    assert admin_fail.status_code == 403

    login_admin = client.post("/auth/login", data={"username": "lead_architect", "password": "AdminSecret456!"})
    admin_token = login_admin.json()["access_token"]
    admin_success = client.get("/admin/dashboard", headers={"Authorization": f"Bearer {admin_token}"})
    assert admin_success.status_code == 200
    assert "Welcome Administrator" in admin_success.json()["message"]

if __name__ == "__main__":
    test_auth_workflow()
    print("ALL TASK 2 JWT & RBAC TESTS PASSED SUCCESSFULLY!")
