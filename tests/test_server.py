from server import app


class TestServer:

    def test_login_with_good_email(self):
        client = app.test_client()
        result = client.post("/showSummary", data=dict(email="john@simplylift.co"))
        assert result.status_code in [200]
        
    def test_login_with_bad_email(self):
        client = app.test_client()
        result = client.post("/showSummary", data=dict(email="aa@aa.aa"))
        assert result.status_code in [500]
