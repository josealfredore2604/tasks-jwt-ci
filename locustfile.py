import uuid
from locust import HttpUser, task, between

class ApiUserWorkflow(HttpUser):
    wait_time = between(1, 3)
    
    token = None
    username = None
    password = "testpassword123"

    def on_start(self):
        
        self.username = f"locustuser_{uuid.uuid4()}"
        try:
            self.client.post(
                "/users", 
                json={"username": self.username, "password": self.password}
            )
            
            response = self.client.post(
                "/token", 
                data={"username": self.username, "password": self.password}
            )
            response_data = response.json()
            
            if "access_token" in response_data:
                self.token = response_data["access_token"]
            else:
                print(f"Error al iniciar sesión para {self.username}")
        
        except Exception as e:
            print(f"Fallo en on_start: {e}")

    @task(3)
    def get_tasks(self):
        if self.token:
            self.client.get(
                "/tasks", 
                headers={"Authorization": f"Bearer {self.token}"}
            )

    @task(1)
    def create_task(self):
        if self.token:
            self.client.post(
                "/tasks",
                headers={"Authorization": f"Bearer {self.token}"},
                json={"title": f"Mi tarea locust - {uuid.uuid4()}"}
            )