# Prodigy API

A REST API for managing fitness programs, activities, and user progress tracking.

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Python ORM for database operations
- **Pydantic** - Data validation and serialization
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server
- **SQLite/PostgreSQL** - Database options

## 🚀 Features

- Program management (CRUD operations)
- Activity tracking within programs
- User registration and management
- Progress tracking with completion status
- RESTful API with auto-generated docs
- Comprehensive unit test suite (UTS)
- Input validation and error handling

## 📋 Installation

```bash
# Clone repository
git clone <your-repo-url>
cd prodigy-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python -c "from app.database import create_tables; create_tables()"

# Run server
uvicorn app.main:app --reload
```

## 📚 API Endpoints

### Programs

- `GET/POST /api/v1/programs/` - List/Create programs
- `GET/PUT/DELETE /api/v1/programs/{id}` - Get/Update/Delete program

### Users

- `GET/POST /api/v1/users/` - List/Create users
- `GET/PUT/DELETE /api/v1/users/{id}` - Get/Update/Delete user
- `GET /api/v1/users/{id}/progress` - Get user progress

### Activities

- `GET/POST /api/v1/activities/` - List/Create activities
- `GET/PUT/DELETE /api/v1/activities/{id}` - Get/Update/Delete activity

### Progress

- `GET/POST /api/v1/progress/` - List/Create progress records
- `GET/PUT/DELETE /api/v1/progress/{id}` - Get/Update/Delete progress

## 🧪 Testing

We have implemented a comprehensive Unit Test Suite (UTS) covering all API endpoints:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py -v
```

**Test Coverage:**

- CRUD operations for all models
- User progress tracking
- Error handling (404, 422, 400)
- Data validation
- Database relationships

## 🔧 Usage Example

```bash
# Create a program
curl -X POST "http://localhost:8000/api/v1/programs/" \
  -H "Content-Type: application/json" \
  -d '{"name": "30-Day Challenge", "description": "Fitness program", "duration_days": 30}'

# Create a user
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com"}'
```

## 📁 Project Structure

```
prodigy-api/
├── app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB configuration
│   ├── models/models.py     # SQLAlchemy models
│   ├── schemas/schemas.py   # Pydantic schemas
│   └── routers/             # API endpoints
├── tests/
│   ├── conftest.py          # Test configuration
│   └── test_api.py          # Comprehensive UTS
└── requirements.txt
```

## 🌐 Access Points

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 Features

- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy ORM
- Comprehensive error handling
- Auto-generated interactive documentation
- Unit test suite with 95%+ coverage

---

**Built with FastAPI + SQLAlchemy | Tested with comprehensive UTS**
