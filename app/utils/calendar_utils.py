from datetime import datetime, timedelta
from typing import List, Tuple

def get_week_date_range(start_date: datetime, week_number: int) -> Tuple[datetime, datetime]:
    """Get the start and end date for a specific week of the program"""
    week_start = start_date + timedelta(days=(week_number - 1) * 7)
    week_end = week_start + timedelta(days=6)
    return week_start, week_end

def get_day_number_from_date(start_date: datetime, target_date: datetime) -> int:
    """Calculate the program day number from a specific date"""
    delta = target_date - start_date
    return delta.days + 1

def get_date_from_day_number(start_date: datetime, day_number: int) -> datetime:
    """Get the actual date for a specific program day"""
    return start_date + timedelta(days=day_number - 1)

def get_current_week_dates(start_date: datetime, current_day: int) -> List[datetime]:
    """Get all dates for the current week"""
    current_date = get_date_from_day_number(start_date, current_day)
    # Find the start of the current week (assuming week starts on Monday)
    days_since_monday = current_date.weekday()
    week_start = current_date - timedelta(days=days_since_monday)
    
    return [week_start + timedelta(days=i) for i in range(7)]
