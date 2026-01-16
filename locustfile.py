from locust import HttpUser, task, between
import random

class SchoolAPIUser(HttpUser):
    host = "http://127.0.0.1:10000"
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Authenticate once per user
        """
        # Try to login with test credentials
        response = self.client.post(
            "/auth/login",
            data={
                "username": "testuser@school.com",
                "password": "password123",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            name="LOGIN"
        )

        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {
                "Authorization": f"Bearer {self.token}"
            }
        else:
            # If login fails, continue without auth
            self.token = None
            self.headers = {}
            print(f"⚠️ Login failed: {response.status_code}")

    # ========== STUDENT ENDPOINTS ==========
    @task(3)
    def get_students(self):
        """Read all students"""
        self.client.get(
            "/students/",
            headers=self.headers,
            name="GET /students"
        )

    @task(2)
    def get_student_detail(self):
        """Read specific student"""
        student_id = random.randint(1, 10)
        self.client.get(
            f"/students/{student_id}",
            headers=self.headers,
            name="GET /students/{id}"
        )

    @task(1)
    def create_student(self):
        """Create a new student"""
        if not self.token:
            return
        self.client.post(
            "/students/",
            json={
                "first_name": f"Student_{random.randint(1000, 9999)}",
                "last_name": "Test",
                "email": f"student{random.randint(1000, 9999)}@school.com",
                "date_of_birth": "2010-01-15",
            },
            headers=self.headers,
            name="POST /students"
        )

    # ========== TEACHER ENDPOINTS ==========
    @task(2)
    def get_teachers(self):
        """Read all teachers"""
        self.client.get(
            "/teachers/",
            headers=self.headers,
            name="GET /teachers"
        )

    @task(1)
    def get_teacher_detail(self):
        """Read specific teacher"""
        teacher_id = random.randint(1, 5)
        self.client.get(
            f"/teachers/{teacher_id}",
            headers=self.headers,
            name="GET /teachers/{id}"
        )

    # ========== NOTIFICATION ENDPOINTS ==========
    @task(2)
    def get_notifications(self):
        """Get notifications"""
        self.client.get(
            "/notifications/",
            headers=self.headers,
            name="GET /notifications"
        )

    # ========== HEALTH CHECK ==========
    @task(5)
    def health_check(self):
        """Health check endpoint"""
        self.client.get(
            "/",
            name="GET /"
        )
