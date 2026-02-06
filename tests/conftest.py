import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and participate in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball games and training",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "marcus@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn instruments and perform in concerts",
            "schedule": "Mondays and Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore STEM topics through experiments and projects",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Clear and reset activities dictionary
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset again after test
    activities.clear()
    activities.update(original_activities)
