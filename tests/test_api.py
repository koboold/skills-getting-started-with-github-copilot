import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that get_activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_get_activities_contains_required_fields(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
    
    def test_get_activities_participants_format(self, client):
        """Test that participants is a list"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        assert isinstance(activity["participants"], list)
        assert "michael@mergington.edu" in activity["participants"]


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_student_success(self, client):
        """Test successful signup for a new student"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
        
        # Verify student was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "newstudent@mergington.edu" in activities_data["Chess Club"]["participants"]
    
    def test_signup_to_nonexistent_activity_fails(self, client):
        """Test signup fails for non-existent activity"""
        response = client.post(
            "/activities/Fake%20Activity/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_student_fails(self, client):
        """Test that duplicate signup fails"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_multiple_students(self, client):
        """Test that multiple different students can sign up"""
        response1 = client.post(
            "/activities/Chess%20Club/signup?email=student1@mergington.edu"
        )
        response2 = client.post(
            "/activities/Chess%20Club/signup?email=student2@mergington.edu"
        )
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both were added
        activities_response = client.get("/activities")
        participants = activities_response.json()["Chess Club"]["participants"]
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants
    
    def test_signup_to_different_activities(self, client):
        """Test that a student can sign up to multiple activities"""
        response1 = client.post(
            "/activities/Chess%20Club/signup?email=student@mergington.edu"
        )
        response2 = client.post(
            "/activities/Programming%20Class/signup?email=student@mergington.edu"
        )
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert "student@mergington.edu" in data["Chess Club"]["participants"]
        assert "student@mergington.edu" in data["Programming Class"]["participants"]


class TestUnregister:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_existing_student_success(self, client):
        """Test successful unregistration of existing student"""
        response = client.post(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert "michael@mergington.edu" in data["message"]
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "michael@mergington.edu" not in activities_data["Chess Club"]["participants"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client):
        """Test unregister fails for non-existent activity"""
        response = client.post(
            "/activities/Fake%20Activity/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_unregister_nonexistent_student_fails(self, client):
        """Test unregister fails for student not in activity"""
        response = client.post(
            "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]
    
    def test_unregister_then_signup_again(self, client):
        """Test that a student can unregister and sign up again"""
        # Unregister
        response1 = client.post(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Sign up again
        response2 = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response2.status_code == 200
        
        # Verify student is in participants
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "michael@mergington.edu" in activities_data["Chess Club"]["participants"]
    
    def test_unregister_all_participants_from_activity(self, client):
        """Test unregistering all participants from an activity"""
        # Unregister all participants from Tennis Club (has 1 participant)
        response = client.post(
            "/activities/Tennis%20Club/unregister?email=alex@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify no participants left
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert len(activities_data["Tennis Club"]["participants"]) == 0


class TestRoot:
    """Tests for GET / endpoint"""
    
    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static HTML"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
