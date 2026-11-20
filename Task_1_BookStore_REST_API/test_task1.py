from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app_id"] == "DT-2026-89H4F"

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) >= 4

def test_filter_books():
    response = client.get("/books?genre=Technology")
    assert response.status_code == 200
    for book in response.json():
        assert book["genre"] == "Technology"

def test_create_and_delete_book():
    new_payload = {
        "title": "FastAPI Microservices in Action",
        "author": "Syed Jawad Hussain Shah",
        "genre": "Technology",
        "price": 34.99,
        "published_year": 2026,
        "stock": 10
    }
    create_resp = client.post("/books", json=new_payload)
    assert create_resp.status_code == 201
    created_id = create_resp.json()["id"]

    get_resp = client.get(f"/books/{created_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "FastAPI Microservices in Action"

    del_resp = client.delete(f"/books/{created_id}")
    assert del_resp.status_code == 204

    get_del_resp = client.get(f"/books/{created_id}")
    assert get_del_resp.status_code == 404

if __name__ == "__main__":
    test_root()
    test_get_books()
    test_filter_books()
    test_create_and_delete_book()
    print("ALL TASK 1 TESTS PASSED SUCCESSFULLY!")
