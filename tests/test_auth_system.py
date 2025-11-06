import requests
import time

BASE_URL = "http://localhost:8000"

test_state = {}

def test_1_health_check():
  time.sleep(5)
  try:
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200
  except requests.ConnectionError:
    print("Connection failed. Is the app running? `docker-compose up -d --build`")
    assert False, "Could not connect to app"

def test_2_get_tasks_unauthorized():
  response = requests.get(f"{BASE_URL}/tasks")
  assert response.status_code == 401

def test_3_register_user():
  user_data = {"username": "testuser", "password": "testpassword"}
  response = requests.post(f"{BASE_URL}/users", json=user_data)
  assert response.status_code == 200
  assert response.json() == {"message": "User testuser registered successfully"}

def test_4_register_user_duplicate():
  user_data = {"username": "testuser", "password": "testpassword"}
  response = requests.post(f"{BASE_URL}/users", json=user_data)
  assert response.status_code == 400
  assert response.json()["detail"] == "Username already registered"

def test_5_login_for_token():
  login_data = {"username": "testuser", "password": "testpassword"}
  response = requests.post(f"{BASE_URL}/token", data=login_data)
  assert response.status_code == 200
  
  data = response.json()
  assert "access_token" in data
  assert data["token_type"] == "bearer"
  
  test_state["token"] = data["access_token"]

def test_6_create_task_with_auth():
  assert "token" in test_state, "Login test must run first"
  
  token = test_state["token"]
  headers = {"Authorization": f"Bearer {token}"}
  
  task_data = {"title": "My Authenticated Task"}
  response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
  
  assert response.status_code == 200
  data = response.json()
  assert data["title"] == "My Authenticated Task"
  assert "id" in data
  
  test_state["task_id"] = data["id"]

def test_7_get_tasks_with_auth():
  token = test_state["token"]
  headers = {"Authorization": f"Bearer {token}"}
  
  response = requests.get(f"{BASE_URL}/tasks", headers=headers)
  assert response.status_code == 200
  
  tasks = response.json()
  assert isinstance(tasks, list)
  assert len(tasks) > 0
  assert tasks[0]["title"] == "My Authenticated Task"

def test_8_delete_task_with_auth():
  token = test_state["token"]
  task_id = test_state["task_id"]
  headers = {"Authorization": f"Bearer {token}"}
  
  response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
  assert response.status_code == 200
  assert response.json() == {"message": "Task deleted"}