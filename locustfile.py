"""
Locust Load Testing for FastAPI Application

This file contains load tests for both Users and BlogPosts APIs.
It simulates realistic user behavior patterns and measures performance.

Run with:
    locust -f locustfile.py --host=http://localhost:8000

Then open http://localhost:8089 to access the Locust web UI.

For headless mode:
    locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 1m --headless
"""

from locust import HttpUser, task, between, SequentialTaskSet
from uuid import uuid4
import random


class UserBehavior(SequentialTaskSet):
    """
    Sequential task set simulating realistic user behavior.
    
    Users will:
    1. List users/posts
    2. Create new resources
    3. Read specific resources
    4. Update resources
    5. Delete resources
    """
    
    created_user_ids = []
    created_post_ids = []
    
    def on_start(self):
        """Initialize test data when user starts."""
        self.user_email = f"loadtest-{uuid4()}@example.com"
        self.post_slug = f"loadtest-{uuid4().hex[:8]}"
    
    @task(2)
    def list_users(self):
        """GET /users/ - List all users with pagination."""
        with self.client.get(
            "/users/",
            params={"skip": 0, "limit": 10},
            catch_response=True,
            name="/users/ [List]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(3)
    def create_user(self):
        """POST /users/ - Create a new user."""
        payload = {
            "email": f"loadtest-{uuid4()}@example.com",
            "password": "TestPass123!",
            "first_name": "Load",
            "last_name": "Test"
        }
        
        with self.client.post(
            "/users/",
            json=payload,
            catch_response=True,
            name="/users/ [Create]"
        ) as response:
            if response.status_code in [200, 201]:
                # Save user ID for later operations
                user_data = response.json()
                self.created_user_ids.append(user_data["id"])
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def get_user(self):
        """GET /users/{user_id} - Get specific user."""
        if self.created_user_ids:
            user_id = random.choice(self.created_user_ids)
            with self.client.get(
                f"/users/{user_id}",
                catch_response=True,
                name="/users/{user_id} [Read]"
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 404:
                    response.success()  # Expected for deleted users
                else:
                    response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def update_user(self):
        """PATCH /users/{user_id} - Update user."""
        if self.created_user_ids:
            user_id = random.choice(self.created_user_ids)
            payload = {
                "first_name": f"Updated-{random.randint(1, 1000)}"
            }
            
            with self.client.patch(
                f"/users/{user_id}",
                json=payload,
                catch_response=True,
                name="/users/{user_id} [Update]"
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 404:
                    response.success()  # Expected for deleted users
                else:
                    response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def list_posts(self):
        """GET /posts/ - List all posts with pagination."""
        with self.client.get(
            "/posts/",
            params={"skip": 0, "limit": 10},
            catch_response=True,
            name="/posts/ [List]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(3)
    def create_post(self):
        """POST /posts/ - Create a new blog post."""
        # Use a random user ID or create a new one
        if self.created_user_ids:
            author_id = random.choice(self.created_user_ids)
        else:
            author_id = str(uuid4())
        
        payload = {
            "title": f"Load Test Post {uuid4().hex[:8]}",
            "slug": f"loadtest-{uuid4().hex[:8]}",
            "content": f"This is a load test post created at {random.randint(1, 100000)}",
            "excerpt": "Load testing excerpt",
            "is_published": random.choice([True, False]),
            "author_id": author_id
        }
        
        with self.client.post(
            "/posts/",
            json=payload,
            catch_response=True,
            name="/posts/ [Create]"
        ) as response:
            if response.status_code in [200, 201]:
                # Save post ID for later operations
                post_data = response.json()
                self.created_post_ids.append(post_data["id"])
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def get_post(self):
        """GET /posts/{post_id} - Get specific post."""
        if self.created_post_ids:
            post_id = random.choice(self.created_post_ids)
            with self.client.get(
                f"/posts/{post_id}",
                catch_response=True,
                name="/posts/{post_id} [Read]"
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 404:
                    response.success()  # Expected for deleted posts
                else:
                    response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def update_post(self):
        """PATCH /posts/{post_id} - Update post."""
        if self.created_post_ids:
            post_id = random.choice(self.created_post_ids)
            payload = {
                "title": f"Updated Post {random.randint(1, 1000)}",
                "is_published": random.choice([True, False])
            }
            
            with self.client.patch(
                f"/posts/{post_id}",
                json=payload,
                catch_response=True,
                name="/posts/{post_id} [Update]"
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 404:
                    response.success()  # Expected for deleted posts
                else:
                    response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def delete_user(self):
        """DELETE /users/{user_id} - Delete user."""
        if self.created_user_ids and len(self.created_user_ids) > 5:
            user_id = self.created_user_ids.pop(random.randint(0, len(self.created_user_ids) - 1))
            with self.client.delete(
                f"/users/{user_id}",
                catch_response=True,
                name="/users/{user_id} [Delete]"
            ) as response:
                if response.status_code in [200, 204]:
                    response.success()
                elif response.status_code == 404:
                    response.success()  # Already deleted
                else:
                    response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def delete_post(self):
        """DELETE /posts/{post_id} - Delete post."""
        if self.created_post_ids and len(self.created_post_ids) > 5:
            post_id = self.created_post_ids.pop(random.randint(0, len(self.created_post_ids) - 1))
            with self.client.delete(
                f"/posts/{post_id}",
                catch_response=True,
                name="/posts/{post_id} [Delete]"
            ) as response:
                if response.status_code in [200, 204]:
                    response.success()
                elif response.status_code == 404:
                    response.success()  # Already deleted
                else:
                    response.failure(f"Got status code {response.status_code}")


class APIUser(HttpUser):
    """
    Simulated user for load testing.
    
    Configuration:
    - wait_time: Random wait between 1-5 seconds between tasks
    - tasks: Uses UserBehavior task set
    """
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    # Add custom headers if needed
    def on_start(self):
        """Called when a simulated user starts."""
        self.client.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Locust Load Test"
        }


class QuickTest(HttpUser):
    """
    Quick smoke test user - hits endpoints rapidly without waiting.
    Use this to quickly verify API can handle high request rates.
    """
    wait_time = between(0.1, 0.5)  # Very short wait times
    
    @task(5)
    def quick_list_users(self):
        """Rapid-fire user listing."""
        self.client.get("/users/?skip=0&limit=5", name="/users/ [Quick]")
    
    @task(5)
    def quick_list_posts(self):
        """Rapid-fire post listing."""
        self.client.get("/posts/?skip=0&limit=5", name="/posts/ [Quick]")
    
    @task(1)
    def quick_create_user(self):
        """Quick user creation."""
        payload = {
            "email": f"quick-{uuid4()}@example.com",
            "password": "Quick123!",
        }
        self.client.post("/users/", json=payload, name="/users/ [Quick Create]")
