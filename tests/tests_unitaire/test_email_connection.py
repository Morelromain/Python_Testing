import server
from server import app


import server
from server import app


class TestEmail:
    """Test server.py using pytest"""

    client_test = app.test_client()
    compets_test = [
        {"name": "compet1",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "5"},
        {"name": "compet2",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"}]
    clubs_test = [{"name": "club1", "email": "club1@email.co", "points": "15"}]

    def setup(self):
        """Change server.py variable data"""

        server.competitions = [
            {"name": "compet1",
                "date": "2022-03-27 10:00:00",
                "numberOfPlaces": "5"},
            {"name": "compet2",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"}]
        server.clubs = [
            {"name": "club1", "email": "club1@email.co", "points": "15"}]

    def test_good_email(self):
        """test login with good email"""

        result = self.client_test.post(
            "/showSummary", data=dict(email="club1@email.co")
            )
        assert result.status_code in [200]

    def test_bad_email(self):
        """test login with bad email"""

        result = self.client_test.post(
            "/showSummary", data=dict(email="aa@aa.aa")
            )
        assert result.status_code in [403]

