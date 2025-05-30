from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class ActivityBase(BaseModel):
    title: str
    description: str
    day_number: int
    duration_minutes: int = 5
    category: str

class ActivityCreate(ActivityBase):
    program_id: int

class Activity(ActivityBase):
    id: int
    program_id: int
    
    class Config:
        from_attributes = True

class ActivityWithCompletion(Activity):
    is_completed: bool = False
    completed_at: Optional[datetime] = None

class ProgramBase(BaseModel):
    name: str
    description: str
    duration_days: int = 30

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int
    created_at: datetime
    activities: List[Activity] = []
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProgressBase(BaseModel):
    program_id: int
    start_date: datetime

class UserProgressCreate(UserProgressBase):
    user_id: int

class UserProgress(UserProgressBase):
    id: int
    user_id: int
    current_day: int
    is_active: bool
    
    class Config:
        from_attributes = True

class DayPlan(BaseModel):
    date: datetime
    day_number: int
    activities: List[ActivityWithCompletion]
    total_activities: int
    completed_activities: int
    completion_percentage: float

class WeekPlan(BaseModel):
    start_date: datetime
    end_date: datetime
    days: List[DayPlan]

class ActivityCompletionRequest(BaseModel):
    activity_id: int
    completion_date: datetime
    