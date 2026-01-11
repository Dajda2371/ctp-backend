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

class ChatGroup(Base):
    __tablename__ = "chat_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True) # Null for DMs
    is_group = Column(Integer, default=0) # 0 for DM, 1 for Group
    created_at = Column(DateTime, default=datetime.utcnow)
    
    members = relationship("ChatMember", back_populates="group")
    messages = relationship("ChatMessage", back_populates="group")

class ChatMember(Base):
    __tablename__ = "chat_members"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("chat_groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    group = relationship("ChatGroup", back_populates="members")
    user = relationship("User")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("chat_groups.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    group = relationship("ChatGroup", back_populates="messages")
    sender = relationship("User")
    files = relationship("ChatFile", back_populates="message")

class ChatFile(Base):
    __tablename__ = "chat_files"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"))
    filename = Column(String)
    content = Column(LargeBinary)
    mime_type = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    message = relationship("ChatMessage", back_populates="files")

class PlannerSettings(Base):
    __tablename__ = "planner_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    start_time = Column(String, default="09:00")
    end_time = Column(String, default="17:00")
    work_days = Column(String, default="0,1,2,3,4") # 0=Mon, 6=Sun
    
    user = relationship("User")

class PlannerEvent(Base):
    __tablename__ = "planner_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    event_type = Column(String) # 'work', 'time_off', 'task'
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    user = relationship("User")
    task = relationship("Task")

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    token = Column(String, primary_key=True, index=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)
