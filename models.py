from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float, LargeBinary
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
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    property_manager = Column(Integer)
    facility_manager = Column(Integer)

    tasks = relationship("Task", back_populates="site")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="TODO") # TODO, IN_PROGRESS, DONE, BLOCKED
    priority = Column(Integer, default=3) # 1 to 5, default 3
    assignee = Column(String) # For now, simple string or FK to users.name
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    photos = Column(JSON, default=[]) # Keeping for backward compatibility or metadata

    site = relationship("Site", back_populates="tasks")
    task_photos = relationship("TaskPhoto", back_populates="task", cascade="all, delete-orphan")

class TaskPhoto(Base):
    __tablename__ = "task_photos"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    filename = Column(String)
    content = Column(LargeBinary)
    mime_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="task_photos")

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    token = Column(String, primary_key=True, index=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)
