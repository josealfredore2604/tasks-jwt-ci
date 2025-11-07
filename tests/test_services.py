from sqlalchemy.orm import Session
from app.services import create_task, get_tasks, delete_task, create_user
from app.models import SessionLocal, User

def get_test_user(db: Session):
  user = db.query(User).filter(User.username == "service_test_user").first()
  if not user:
    user = create_user(db, "service_test_user", "password")
  return user

def test_create_task():
  db = SessionLocal()
  test_user = get_test_user(db)
  
  task = create_task(db, "Test Task", user_id=test_user.id)
  
  assert task.title == "Test Task"
  assert task.owner_id == test_user.id
  db.close()

def test_get_tasks():
  db = SessionLocal()
  test_user = get_test_user(db)
  
  tasks = get_tasks(db, user_id=test_user.id)
  
  assert isinstance(tasks, list)
  db.close()

def test_delete_task():
  db = SessionLocal()
  test_user = get_test_user(db)
  
  task = create_task(db, "Task to Delete", user_id=test_user.id)
  deleted_task = delete_task(db, task.id, user_id=test_user.id)
  
  assert deleted_task is not None
  db.close()