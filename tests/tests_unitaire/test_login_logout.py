from server import app


class TestLog:
    """Test server.py using pytest"""

    client_test = app.test_client()

    def test_index(self):
        """ test acces to index page """

        result = self.client_test.get("/")
        assert result.status_code in [200]

    def test_logout(self):
        """ test acces to logout page """

        result = self.client_test.get("logout")
        assert result.status_code in [302]
