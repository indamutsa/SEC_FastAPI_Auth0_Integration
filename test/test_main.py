import os
from fastapi.testclient import TestClient
from application.models import TodoItem, TodoCreate
from application.main import app

os.environ['TEST_ENV'] = 'True'
client = TestClient(app)


def test_create_todo():

    response = client.post("/api/todos/", json={"name": "Test Todo", "completed": False})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Todo"
    assert not data["completed"]
    assert "id" in data

def test_update_todo():
    create_response = client.post("/api/todos/", json={"name": "Initial Todo", "completed": False})
    assert create_response.status_code == 200, create_response.text
    todo_id = create_response.json()["id"]
    
    update_response = client.put(f"/api/todos/{todo_id}", json={"name": "Updated Todo", "completed": True})
    assert update_response.status_code == 200, update_response.text
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Todo"
    assert updated_data["completed"]

def test_delete_todo():
    create_response = client.post("/api/todos/", json={"name": "To Delete", "completed": False})
    assert create_response.status_code == 200, create_response.text
    todo_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200, delete_response.text
    delete_message = delete_response.json()
    assert delete_message == {"message": "Todo deleted successfully"}

    get_response = client.get("/api/todos/")
    assert all(todo["id"] != todo_id for todo in get_response.json()), get_response.text
