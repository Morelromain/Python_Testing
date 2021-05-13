import server
from server import app


class TestDisplayPlace:
    """Test server.py using pytest"""

    client_test = app.test_client()

    def setup(self):
        """Change server.py variable data"""

        server.competitions = [
            {"name": "compet1",
                "date": "2022-03-27 10:00:00",
                "numberOfPlaces": "5"}]
        server.clubs = [
            {"name": "club1", "email": "club1@email.co", "points": "15"}]

    def test_display_board_with_book_place(self):
        """test book a place and display the modified data in board"""

        result = self.client_test.post(
            "/purchasePlaces", data={
                "places": 1,
                "club": "club1",
                "competition": "compet1"}
        )
        assert result.status_code in [200]
        assert "<td>club1</td>"in result.data.decode()
        assert "<td>12</td>" in result.data.decode()
        assert "compet1" in result.data.decode()
