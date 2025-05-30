import pytest
from datetime import datetime, timedelta
from app.models.models import Program, Activity, User, UserProgress

class TestProdigyAPI:
    
    def test_create_program(self, client):
        program_data = {
            "name": "30-Day Fitness Challenge",
            "description": "A comprehensive 30-day fitness program",
            "duration_days": 30
        }
        response = client.post("/api/v1/programs/", json=program_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == program_data["name"]
        assert data["duration_days"] == 30

    def test_create_user(self, client):
        user_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_programs(self, client):
        # First create a program
        program_data = {
            "name": "Test Program",
            "description": "Test description",
            "duration_days": 14
        }
        client.post("/api/v1/programs/", json=program_data)
        
        # Then retrieve all programs
        response = client.get("/api/v1/programs/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_program_by_id(self, client):
        # Create a program first
        program_data = {
            "name": "Specific Program",
            "description": "Specific description",
            "duration_days": 21
        }
        create_response = client.post("/api/v1/programs/", json=program_data)
        program_id = create_response.json()["id"]
        
        # Retrieve the specific program
        response = client.get(f"/api/v1/programs/{program_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Specific Program"
        assert data["id"] == program_id

    def test_create_activity(self, client):
        # First create a program
        program_data = {
            "name": "Program for Activities",
            "description": "Test program",
            "duration_days": 7
        }
        program_response = client.post("/api/v1/programs/", json=program_data)
        program_id = program_response.json()["id"]
        
        # Create an activity
        activity_data = {
            "name": "Push-ups",
            "description": "Do 20 push-ups",
            "program_id": program_id,
            "day_number": 1
        }
        response = client.post("/api/v1/activities/", json=activity_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Push-ups"
        assert data["program_id"] == program_id

    def test_user_progress_tracking(self, client):
        # Create user
        user_data = {
            "username": "progressuser",
            "email": "progress@example.com"
        }
        user_response = client.post("/api/v1/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        # Create program and activity
        program_data = {
            "name": "Progress Program",
            "description": "Test progress tracking",
            "duration_days": 5
        }
        program_response = client.post("/api/v1/programs/", json=program_data)
        program_id = program_response.json()["id"]
        
        activity_data = {
            "name": "Daily Walk",
            "description": "Walk for 30 minutes",
            "program_id": program_id,
            "day_number": 1
        }
        activity_response = client.post("/api/v1/activities/", json=activity_data)
        activity_id = activity_response.json()["id"]
        
        # Track progress
        progress_data = {
            "user_id": user_id,
            "activity_id": activity_id,
            "completed": True,
            "notes": "Completed successfully"
        }
        response = client.post("/api/v1/progress/", json=progress_data)
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == True
        assert data["user_id"] == user_id

    def test_get_user_progress(self, client):
        # Create user
        user_data = {
            "username": "trackuser",
            "email": "track@example.com"
        }
        user_response = client.post("/api/v1/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        # Get user progress
        response = client.get(f"/api/v1/users/{user_id}/progress")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_invalid_program_creation(self, client):
        # Test with missing required fields
        invalid_data = {
            "name": "Incomplete Program"
            # Missing description and duration_days
        }
        response = client.post("/api/v1/programs/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_nonexistent_program_retrieval(self, client):
        # Try to get a program that doesn't exist
        response = client.get("/api/v1/programs/999999")
        assert response.status_code == 404

    def test_duplicate_user_creation(self, client):
        # Create a user
        user_data = {
            "username": "duplicate",
            "email": "duplicate@example.com"
        }
        first_response = client.post("/api/v1/users/", json=user_data)
        assert first_response.status_code == 200
        
        # Try to create the same user again
        second_response = client.post("/api/v1/users/", json=user_data)
        assert second_response.status_code == 400  # Conflict/Bad Request

    def test_update_program(self, client):
        # Create a program
        program_data = {
            "name": "Original Program",
            "description": "Original description",
            "duration_days": 10
        }
        create_response = client.post("/api/v1/programs/", json=program_data)
        program_id = create_response.json()["id"]
        
        # Update the program
        update_data = {
            "name": "Updated Program",
            "description": "Updated description",
            "duration_days": 15
        }
        response = client.put(f"/api/v1/programs/{program_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Program"
        assert data["duration_days"] == 15

    def test_delete_program(self, client):
        # Create a program
        program_data = {
            "name": "Program to Delete",
            "description": "Will be deleted",
            "duration_days": 7
        }
        create_response = client.post("/api/v1/programs/", json=program_data)
        program_id = create_response.json()["id"]
        
        # Delete the program
        response = client.delete(f"/api/v1/programs/{program_id}")
        assert response.status_code == 200
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/programs/{program_id}")
        assert get_response.status_code == 404

    def test_program_activities_endpoint(self, client):
        # Create program
        program_data = {
            "name": "Program with Activities",
            "description": "Has multiple activities",
            "duration_days": 5
        }
        program_response = client.post("/api/v1/programs/", json=program_data)
        program_id = program_response.json()["id"]
        
        # Create multiple activities
        for i in range(3):
            activity_data = {
                "name": f"Activity {i+1}",
                "description": f"Description {i+1}",
                "program_id": program_id,
                "day_number": i+1
            }
            client.post("/api/v1/activities/", json=activity_data)
        
        # Get all activities for the program
        response = client.get(f"/api/v1/programs/{program_id}/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        