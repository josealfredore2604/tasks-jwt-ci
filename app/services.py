from sqlalchemy.orm import Session
from . import models
from . import auth

def get_user_by_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str):
  hashed_password = auth.get_password_hash(password)
  db_user = models.User(username=username, hashed_password=hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def create_task(db: Session, title: str, user_id: int): 
  task = models.Task(title=title, owner_id=user_id) 
  db.add(task)
  db.commit()
  db.refresh(task)
  return task

def get_tasks(db: Session, user_id: int): 
  return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def delete_task(db: Session, task_id: int, user_id: int): 
  task = db.query(models.Task).filter(
    models.Task.id == task_id, 
    models.Task.owner_id == user_id
  ).first()
  
  if not task:
    return None
  
  db.delete(task)
  db.commit()
  return task