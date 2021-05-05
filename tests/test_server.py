import server
from server import app


class TestServer:
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

# bug 1
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

# bug 2
    def test_less_place(self):
        """test less place request than place of competition"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.compets_test[0]["numberOfPlaces"]) - 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[0]["name"]}
        )
        assert result.status_code in [200]

    def test_more_place(self):
        """test more place request than place of competition"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.compets_test[0]["numberOfPlaces"])+1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[0]["name"]}
        )
        assert result.status_code in [403]
        assert "More place request" in result.data.decode()

# bug 3
    def test_less_12(self):
        """test less place request than 12"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": 5,
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

# bug 4
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

# bug 5
    def test_less_club_point(self):
        """test less place request than points club"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.clubs_test[0]["points"]) // 3 - 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[1]["name"]}
        )
        assert result.status_code in [200]

    def test_more_club_point(self):
        """test more place request than points club"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": int(self.clubs_test[0]["points"]) // 3 + 1,
                "club": self.clubs_test[0]["name"],
                "competition": self.compets_test[1]["name"]}
        )
        assert result.status_code in [403]
        assert "More place request than club" in result.data.decode()
