import server
from server import app


class TestNegative:
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

    def test_not_negatif(self):
        """ test place isn't negative """

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": -1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[0]["name"]}
        )
        assert result.status_code in [403]
        assert "negative value" in result.data.decode()