from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)

  tasks = relationship("Task", back_populates="owner")

class Task(Base):
  __tablename__ = "tasks"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  owner_id = Column(Integer, ForeignKey("users.id"))
  
  owner = relationship("User", back_populates="tasks")

def create_tables():
  Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()