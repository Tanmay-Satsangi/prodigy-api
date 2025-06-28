from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database.database import get_db
from app.models.models import Program, Activity, User, UserProgress, UserActivityCompletion
from app.schemas.schemas import (
    Program as ProgramSchema, ProgramCreate,
    Activity as ActivitySchema, ActivityCreate, ActivityWithCompletion,
    User as UserSchema, UserCreate,
    UserProgress as UserProgressSchema, UserProgressCreate,
    DayPlan, WeekPlan, ActivityCompletionRequest
)
from app.utils.calendar_utils import (
    get_week_date_range, get_day_number_from_date, 
    get_date_from_day_number, get_current_week_dates
)

router = APIRouter()

@router.post("/programs/", response_model=ProgramSchema)
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    db_program = Program(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

@router.get("/programs/", response_model=List[ProgramSchema])
def get_programs(db: Session = Depends(get_db)):
    return db.query(Program).all()

@router.get("/programs/{program_id}", response_model=ProgramSchema)
def get_program(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
# But FastAPI sees that you’ve declared response_model=ProgramSchema, so it uses Pydantic to convert the SQLAlchemy object to a JSON-compatible dict.
#     return program

# Activity endpoints
@router.post("/activities/", response_model=ActivitySchema)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

# User endpoints
@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# User Progress endpoints
@router.post("/user-progress/", response_model=UserProgressSchema)
def start_program(progress: UserProgressCreate, db: Session = Depends(get_db)):
    # Check if user already has active progress for this program
    existing = db.query(UserProgress).filter(
        UserProgress.user_id == progress.user_id,
        UserProgress.program_id == progress.program_id,
        UserProgress.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User already has active progress for this program")
    
    db_progress = UserProgress(**progress.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

# Main API: Get Day Plan
@router.get("/users/{user_id}/programs/{program_id}/day-plan", response_model=DayPlan)
def get_day_plan(
    user_id: int, 
    program_id: int, 
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    # Get user progress
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.program_id == program_id,
        UserProgress.is_active == True
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="User progress not found")
    
    # Determine target date
    if date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        target_date = datetime.now().date()
        target_date = datetime.combine(target_date, datetime.min.time())
    
    # Calculate day number
    day_number = get_day_number_from_date(progress.start_date, target_date)
    
    if day_number < 1 or day_number > 30:
        raise HTTPException(status_code=400, detail="Date is outside program duration")
    
    # Get activities for this day
    activities = db.query(Activity).filter(
        Activity.program_id == program_id,
        Activity.day_number == day_number
    ).all()
    
    # Get user completions for this date
    completions = db.query(UserActivityCompletion).filter(
        UserActivityCompletion.user_id == user_id,
        UserActivityCompletion.completion_date >= target_date,
        UserActivityCompletion.completion_date < target_date + timedelta(days=1)
    ).all()
    
    completed_activity_ids = {comp.activity_id for comp in completions}
    completion_map = {comp.activity_id: comp.completed_at for comp in completions}
    
    # Build activities with completion status
    activities_with_completion = []
    for activity in activities:
        activity_dict = {
            "id": activity.id,
            "program_id": activity.program_id,
            "title": activity.title,
            "description": activity.description,
            "day_number": activity.day_number,
            "duration_minutes": activity.duration_minutes,
            "category": activity.category,
            "is_completed": activity.id in completed_activity_ids,
            "completed_at": completion_map.get(activity.id)
        }
        activities_with_completion.append(ActivityWithCompletion(**activity_dict))
    
    # Calculate completion stats
    total_activities = len(activities_with_completion)
    completed_activities = len([a for a in activities_with_completion if a.is_completed])
    completion_percentage = (completed_activities / total_activities * 100) if total_activities > 0 else 0
    
    return DayPlan(
        date=target_date,
        day_number=day_number,
        activities=activities_with_completion,
        total_activities=total_activities,
        completed_activities=completed_activities,
        completion_percentage=completion_percentage
    )

# Main API: Get Week Plan (Days 14-21)
@router.get("/users/{user_id}/programs/{program_id}/week-plan", response_model=WeekPlan)
def get_week_plan(
    user_id: int, 
    program_id: int, 
    week: int = Query(3, description="Week number (1-4), default is week 3 (days 14-21)"),
    db: Session = Depends(get_db)
):
    # Get user progress
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.program_id == program_id,
        UserProgress.is_active == True
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="User progress not found")
    
    if week < 1 or week > 4:
        raise HTTPException(status_code=400, detail="Week must be between 1 and 4")
    
    # Calculate week date range
    week_start, week_end = get_week_date_range(progress.start_date, week)
    
    # Get day plans for each day of the week
    days = []
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        day_number = get_day_number_from_date(progress.start_date, current_date)
        
        if day_number > 30:  # Skip days beyond program duration
            break
            
        # Get activities for this day
        activities = db.query(Activity).filter(
            Activity.program_id == program_id,
            Activity.day_number == day_number
        ).all()
        
        # Get completions for this date
        completions = db.query(UserActivityCompletion).filter(
            UserActivityCompletion.user_id == user_id,
            UserActivityCompletion.completion_date >= current_date,
            UserActivityCompletion.completion_date < current_date + timedelta(days=1)
        ).all()
        
        completed_activity_ids = {comp.activity_id for comp in completions}
        completion_map = {comp.activity_id: comp.completed_at for comp in completions}
        
        # Build activities with completion status
        activities_with_completion = []
        for activity in activities:
            activity_dict = {
                "id": activity.id,
                "program_id": activity.program_id,
                "title": activity.title,
                "description": activity.description,
                "day_number": activity.day_number,
                "duration_minutes": activity.duration_minutes,
                "category": activity.category,
                "is_completed": activity.id in completed_activity_ids,
                "completed_at": completion_map.get(activity.id)
            }
            activities_with_completion.append(ActivityWithCompletion(**activity_dict))
        
        # Calculate completion stats
        total_activities = len(activities_with_completion)
        completed_activities = len([a for a in activities_with_completion if a.is_completed])
        completion_percentage = (completed_activities / total_activities * 100) if total_activities > 0 else 0
        
        day_plan = DayPlan(
            date=current_date,
            day_number=day_number,
            activities=activities_with_completion,
            total_activities=total_activities,
            completed_activities=completed_activities,
            completion_percentage=completion_percentage
        )
        days.append(day_plan)
    
    return WeekPlan(
        start_date=week_start,
        end_date=week_end,
        days=days
    )

# Mark Activity as Complete
@router.post("/users/{user_id}/complete-activity")
def complete_activity(
    user_id: int,
    completion: ActivityCompletionRequest,
    db: Session = Depends(get_db)
):
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.id == completion.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if already completed on this date
    existing = db.query(UserActivityCompletion).filter(
        UserActivityCompletion.user_id == user_id,
        UserActivityCompletion.activity_id == completion.activity_id,
        UserActivityCompletion.completion_date >= completion.completion_date,
        UserActivityCompletion.completion_date < completion.completion_date + timedelta(days=1)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Activity already completed for this date")
    
    # Create completion record
    db_completion = UserActivityCompletion(
        user_id=user_id,
        activity_id=completion.activity_id,
        completion_date=completion.completion_date
    )
    db.add(db_completion)
    db.commit()
    
    return {"message": "Activity marked as complete", "completed_at": db_completion.completed_at}

# Get User's Program Progress Summary
@router.get("/users/{user_id}/programs/{program_id}/progress-summary")
def get_progress_summary(user_id: int, program_id: int, db: Session = Depends(get_db)):
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.program_id == program_id,
        UserProgress.is_active == True
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="User progress not found")
    
    # Calculate total completions
    total_completions = db.query(UserActivityCompletion).filter(
        UserActivityCompletion.user_id == user_id
    ).join(Activity).filter(Activity.program_id == program_id).count()
    
    # Calculate total activities up to current day
    current_day = get_day_number_from_date(progress.start_date, datetime.now())
    if current_day > 30:
        current_day = 30
    
    total_activities = db.query(Activity).filter(
        Activity.program_id == program_id,
        Activity.day_number <= current_day
    ).count()
    
    completion_rate = (total_completions / total_activities * 100) if total_activities > 0 else 0
    
    return {
        "user_id": user_id,
        "program_id": program_id,
        "start_date": progress.start_date,
        "current_day": current_day,
        "total_activities": total_activities,
        "completed_activities": total_completions,
        "completion_rate": completion_rate,
        "is_active": progress.is_active
    }