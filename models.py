from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float
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
    coordinator = Column(String)

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
    photos = Column(JSON, default=[])

    site = relationship("Site", back_populates="tasks")

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    token = Column(String, primary_key=True, index=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)
