import server
from server import app


class TestAgeCompet:
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
            
    def test_new_competition(self):
        """test open competition request"""

        result = self.client_test.get(
            "/book/" + self.compets_test[0]['name']
            + "/" + self.clubs_test[0]['name']
        )
        assert result.status_code in [200]

    def test_old_competition(self):
        """test close competition request"""

        result = self.client_test.get(
            "/book/" + self.compets_test[1]['name']
            + "/" + self.clubs_test[0]['name']
        )
        assert result.status_code in [403]
        assert "the competition is closed" in result.data.decode()