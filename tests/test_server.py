import json

import server


class TestServer:
    
    client = server.app.test_client()
    competitions = [
        {"name": "compet1", "date": "2022-03-27 10:00:00", "numberOfPlaces": "10"},
        {"name": "compet2", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"}
        ]
    clubs = [{"name": "club1", "email": "club1@email.co", "points": "15"}]

    def setup_method(self):

        server.competitions = [
        {"name": "compet1", "date": "2022-03-27 10:00:00", "numberOfPlaces": "10"},
        {"name": "compet2", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"}]
        server.clubs = [{"name": "club1", "email": "club1@email.co", "points": "15"}]


    # bug 1

    def test_good_email(self):
        """test login with good email"""

        result = self.client.post("/showSummary", data=dict(email="club1@email.co"))
        assert result.status_code in [200]
        
    def test_bad_email(self):
        """test login with bad email"""

        result = self.client.post("/showSummary", data=dict(email="aa@aa.aa"))
        assert result.status_code in [500]


    # bug 2

    def test_less_place(self):
        """less place request than place of competition"""

        result = self.client.post(
            "/purchasePlaces", data={
                "places": int(self.competitions[0]["numberOfPlaces"]) - 1,
                "club": self.clubs[0]["name"],
                "competition": self.competitions[0]["name"]}
        )
        assert result.status_code in [200]

    def test_more_place(self):
        """more place request than place of competition"""

        
        result = self.client.post(
            "/purchasePlaces", data={
                "places": int(self.competitions[0]["numberOfPlaces"])+1,
                "club": self.clubs[0]["name"],
                "competition": self.competitions[0]["name"]}
        )
        assert result.status_code in [403]
        assert "More place request" in result.data.decode()


    # bug 3

    def test_less_12(self):
        """BLABLA"""

        result = self.client.post(
            "/purchasePlaces", data={
                "places": 5, 
                "club": self.clubs[0]["name"], 
                "competition": self.competitions[1]["name"]}
        )
        assert result.status_code in [200]

    def test_more_than_12(self):
        """more place request than place of competition"""

        result = self.client.post(
            "/purchasePlaces", data={
                "places": 15,
                "club": self.clubs[0]["name"],
                "competition": self.competitions[1]["name"]}
        )
        assert result.status_code in [403]
        assert "More place than" in result.data.decode()
