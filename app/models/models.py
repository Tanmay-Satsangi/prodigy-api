from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    duration_days = Column(Integer, default=30)
    created_at = Column(DateTime, server_default=func.now())
    
    activities = relationship("Activity", back_populates="program")
    user_progress = relationship("UserProgress", back_populates="program")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    title = Column(String, index=True)
    description = Column(Text)
    day_number = Column(Integer)  # Day 1-30 for month-long program
    duration_minutes = Column(Integer, default=5)
    category = Column(String)  # e.g., "Exercise", "Meditation", "Reading"
    
    program = relationship("Program", back_populates="activities")
    user_completions = relationship("UserActivityCompletion", back_populates="activity")


# USer details table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    
    progress = relationship("UserProgress", back_populates="user")
    completions = relationship("UserActivityCompletion", back_populates="user")

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    start_date = Column(DateTime)
    current_day = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="progress")
    program = relationship("Program", back_populates="user_progress")

class UserActivityCompletion(Base):
    __tablename__ = "user_activity_completions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))
    completed_at = Column(DateTime, server_default=func.now())
    completion_date = Column(DateTime)  # Date for which this activity was completed
    
    user = relationship("User", back_populates="completions")
    activity = relationship("Activity", back_populates="user_completions")
    