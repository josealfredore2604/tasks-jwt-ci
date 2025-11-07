from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .models import create_tables, User, get_db
from .services import (
  create_task, get_tasks, delete_task, 
  get_user_by_username, create_user
)
from .auth import (
  create_access_token, get_current_user, 
  verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI()

create_tables()

@app.post("/users", response_model=dict)
async def register_user(request: Request, db: Session = Depends(get_db)):
  body = await request.json()
  username = body.get("username")
  password = body.get("password")

  if not username or not password:
    raise HTTPException(status_code=400, detail="Username and password are required")
  
  db_user = get_user_by_username(db, username=username)
  if db_user:
    raise HTTPException(status_code=400, detail="Username already registered")
  
  create_user(db=db, username=username, password=password)
  return {"message": f"User {username} registered successfully"}

@app.post("/token", response_model=dict)
async def login_for_access_token(
  form_data: OAuth2PasswordRequestForm = Depends(), 
  db: Session = Depends(get_db)
):
  user = get_user_by_username(db, username=form_data.username)
  
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  
  access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
  access_token = create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks")
async def create_task_endpoint(
  request: Request, 
  db: Session = Depends(get_db), 
  current_user: User = Depends(get_current_user)
):
  body = await request.json()
  title = body.get("title")

  if not title:
    raise HTTPException(status_code=400, detail="Title is required")

  return create_task(db, title, user_id=current_user.id)

@app.get("/tasks")
def get_tasks_endpoint(
  db: Session = Depends(get_db), 
  current_user: User = Depends(get_current_user)
):
  return get_tasks(db, user_id=current_user.id)

@app.delete("/tasks/{task_id}")
def delete_task_endpoint(
  task_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  task = delete_task(db, task_id, user_id=current_user.id)
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")
  return {"message": "Task deleted"}