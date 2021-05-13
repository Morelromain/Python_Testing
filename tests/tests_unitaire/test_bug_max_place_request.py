import server
from server import app


class TestPlaceRequest:
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

    def test_less_12(self):
        """test less place request than 12"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[1]["name"]}
        )
        assert result.status_code in [200]

    def test_more_than_12(self):
        """test more place request than 12"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": 15,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[1]["name"]}
        )
        assert result.status_code in [403]
        assert "More place than" in result.data.decode()

