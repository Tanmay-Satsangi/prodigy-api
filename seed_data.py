from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.models import Program, Activity, User, UserProgress, UserActivityCompletion
from app.database.database import SessionLocal

db: Session = SessionLocal()

# Clear existing data carefully
db.query(UserActivityCompletion).delete()
db.query(UserProgress).delete()
db.query(Activity).delete()
db.query(Program).delete()
db.query(User).delete()
db.commit()

# 1. Create 7 Users with proper names and emails
users_data = [
    ("Alice Smith", "alice.smith@example.com"),
    ("Bob Johnson", "bob.johnson@example.com"),
    ("Charlie Lee", "charlie.lee@example.com"),
    ("Diana King", "diana.king@example.com"),
    ("Ethan Wright", "ethan.wright@example.com"),
    ("Fiona Scott", "fiona.scott@example.com"),
    ("George Martin", "george.martin@example.com"),
]

users = []
for full_name, email in users_data:
    username = full_name.lower().replace(" ", ".")
    user = User(username=username, email=email)
    db.add(user)
    users.append(user)
db.commit()

# 2. Create 7 Programs with descriptions
programs_data = [
    ("Mindful Meditation", "A 30-day journey to mindfulness and relaxation."),
    ("30-Day Fitness Challenge", "Daily exercises to boost your fitness."),
    ("Daily Reading Habit", "Build a habit of reading every day."),
    ("Healthy Eating Plan", "Simple steps to improve your diet."),
    ("Stress Relief Journey", "Techniques to reduce stress."),
    ("Morning Productivity Boost", "Start your day energized and focused."),
    ("Self-Confidence Builder", "Activities to build your confidence."),
]

programs = []
for name, desc in programs_data:
    program = Program(name=name, description=desc, duration_days=30)
    db.add(program)
    programs.append(program)
db.commit()

# 3. Create 7 Activities - One per program, day 1 for simplicity
activities_data = [
    ("Mindful Breathing", "Focus on your breath for 5 minutes.", 1, "Mindfulness"),
    ("Jumping Jacks", "Do jumping jacks for 5 minutes.", 1, "Exercise"),
    ("Read a Chapter", "Read one chapter from a book.", 1, "Reading"),
    ("Eat a Salad", "Include a fresh salad in your meal.", 1, "Nutrition"),
    ("Deep Relaxation", "Spend 5 minutes relaxing your muscles.", 1, "Relaxation"),
    ("Plan Your Day", "Make a to-do list for the day.", 1, "Productivity"),
    ("Positive Affirmations", "Say positive affirmations aloud.", 1, "Confidence"),
]

activities = []
for i, (title, desc, day, category) in enumerate(activities_data):
    activity = Activity(
        title=title,
        description=desc,
        day_number=day,
        program_id=programs[i].id,
        duration_minutes=5,
        category=category,
    )
    db.add(activity)
    activities.append(activity)
db.commit()

# 4. Create 7 UserProgress entries - Each user enrolled in a different program
start_date = datetime.utcnow() - timedelta(days=5)
user_progress_list = []
for i, user in enumerate(users):
    progress = UserProgress(
        user_id=user.id,
        program_id=programs[i].id,
        start_date=start_date,
        current_day=1,
        is_active=True,
    )
    db.add(progress)
    user_progress_list.append(progress)
db.commit()

# 5. Create 7 UserActivityCompletion - Each user completed the activity of their program
for i, user in enumerate(users):
    completion = UserActivityCompletion(
        user_id=user.id,
        activity_id=activities[i].id,
        completed_at=datetime.utcnow(),
        completion_date=datetime.utcnow().date(),
    )
    db.add(completion)
db.commit()

print("✅ Seeded 7 rows in each table with meaningful data.")
