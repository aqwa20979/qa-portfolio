from locust import HttpUser, task, between

class APILoadTest(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_all_posts(self):
        self.client.get("/posts")
    
    @task(1)
    def get_single_post(self):
        self.client.get("/posts/1")
    
    @task(2)
    def create_post(self):
        self.client.post("/posts", json={
            "title": "Load test post",
            "body": "This post was created during load testing",
            "userId": 1
        })