import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    club  = "Simply Lift"
    competition = "Spring Festival"

    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get(f"/book/{self.competition}/{self.club}")

    @task
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", {"places": 0, "club": "Simply Lift", "competition": "Spring Festival"})

