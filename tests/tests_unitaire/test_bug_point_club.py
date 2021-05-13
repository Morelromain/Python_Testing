import server
from server import app


class TestPointClub:
    """Test server.py using pytest"""

    client_test = app.test_client()
    compets_test = [
        {"name": "compet1",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "5"},
        {"name": "compet2",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"},
        {"name": "compet3",
            "date": "2022-03-27 10:00:00",
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
                "numberOfPlaces": "25"},
            {"name": "compet3",
                "date": "2022-03-27 10:00:00",
                "numberOfPlaces": "25"}]
        server.clubs = [
            {"name": "club1", "email": "club1@email.co", "points": "15"}]
    
    
    def test_less_club_point(self):
        """test less place request than points club"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.clubs_test[0]["points"]) // 3 - 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[2]["name"]}
        )
        assert result.status_code in [200]

    def test_more_club_point(self):
        """test more place request than points club"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.clubs_test[0]["points"]) // 3 + 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[2]["name"]}
        )
        assert result.status_code in [403]
        assert "More place request than club" in result.data.decode()