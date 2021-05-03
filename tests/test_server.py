
import json

from server import app, loadClubs, negatif_place, competitions, clubs


class TestServer:

    client = app.test_client()

    # bug 1

    def test_good_email(self):
        """test login with good email"""

        result = self.client.post("/showSummary", data=dict(email="john@simplylift.co"))
        assert result.status_code in [200]
        
    def test_bad_email(self):
        """test login with bad email"""

        result = self.client.post("/showSummary", data=dict(email="aa@aa.aa"))
        assert result.status_code in [500]

    # bug 2

    def test_less_place(self):
        """less place request than place of competition"""

        for competition in competitions:
            result = self.client.post(
                "/purchasePlaces",
                data={
                    "places": int(competition["numberOfPlaces"])-1,
                    "club": clubs[0]["name"],
                    "competition": competition["name"],
                },
            )
            assert result.status_code in [200]


    def test_more_place(self):
        """more place request than place of competition"""

        for competition in competitions:
            result = self.client.post(
                "/purchasePlaces",
                data={
                    "places": int(competition["numberOfPlaces"])+1,
                    "club": clubs[0]["name"],
                    "competition": competition["name"],
                },
            )
            assert result.status_code in [500]
            assert (
                "More place request" in result.data.decode()
                )
