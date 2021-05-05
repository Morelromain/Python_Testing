from locust import HttpUser, task, between

from server import loadClubs, loadCompetitions


competition = loadCompetitions()[0]["name"]
club = loadClubs()[0]["name"]
email = loadClubs()[0]["email"]


class QuickstartUser(HttpUser):
    """ Test server.py using locustfile"""

    wait_time = between(1, 2.5)

    def on_start(self):
        """ Test index acces"""

        self.client.get("/")

    @task
    def post_showSummary(self):
        """ Test showSummary acces and post"""

        self.client.post("/showSummary", data={
            "email": email
            })

    @task
    def get_book(self):
        """ Test book acces"""

        self.client.get("/book/" + competition + "/" + club)

    @task
    def post_purchasePlaces(self):
        """ Test purchasePlaces acces and post"""

        self.client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": 0
            })
