from locust import HttpUser, task, between

from server import loadClubs, loadCompetitions


class LocustServer(HttpUser):
    """ Test server.py using locustfile"""

    wait_time = between(1, 2.5)
    competition = loadCompetitions()[0]["name"]
    club = loadClubs()[0]["name"]
    email = loadClubs()[0]["email"]


    def on_start(self):
        """ Test index acces and showSummary acces and post """

        self.client.get("/", name="index")

        self.client.post("/showSummary", data={
            "email": self.email
            }, name="showSummary")


    @task
    def get_book(self):
        """ Test book acces"""

        self.client.get("/book/" + self.competition 
        + "/" + self.club, name="book")


    @task
    def post_purchasePlaces(self):
        """ Test purchasePlaces acces and post"""

        self.client.post("/purchasePlaces", data={
            "club": self.club,
            "competition": self.competition,
            "places": 0,
            }, name="purchasePlaces")
