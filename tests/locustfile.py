import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    
    def on_start(self):
        self.client.get("")
        self.client.post("showSummary", {"email": "john@simplylift.co"})

    @task
    def essai(self):
        pass