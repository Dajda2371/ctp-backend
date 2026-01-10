from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String, default="technician")
    hashed_password = Column(String)

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    coordinator = Column(String)

    tasks = relationship("Task", back_populates="site")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="TODO") # TODO, IN_PROGRESS, DONE, BLOCKED
    priority = Column(String, default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    assignee = Column(String) # For now, simple string or FK to users.name
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    photos = Column(JSON, default=[])

    site = relationship("Site", back_populates="tasks")
