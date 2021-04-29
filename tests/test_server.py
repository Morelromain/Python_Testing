import json

from server import app, loadClubs, negatif_place

class TestServer:

    client = app.test_client()

    def mock_load_club():
        return [{'name': 'test', 'email': 'good@mail.co'}]

    # test connection with email 

    def test_login_with_good_email(self):
        result = TestServer.client.post("/showSummary", data=dict(email="john@simplylift.co"))
        assert result.status_code in [200]
        
    def test_login_with_bad_email(self):
        result = TestServer.client.post("/showSummary", data=dict(email="aa@aa.aa"))
        assert result.status_code in [500]

    # test found email in club

    def test_found_good_email(self):
        
        def mock_request_email():
            return 'good@mail.co'

        clubs = TestServer.mock_load_club() 
        club = [club for club in clubs if club['email'] == mock_request_email()][0]
        assert club == {'email': 'good@mail.co', 'name': 'test'}
        
    def test_found_bad_email(self):
        
        def mock_request_email():
            return 'bad@mail.co'

        clubs = TestServer.mock_load_club() 
        try:
            club = [club for club in clubs if club['email'] == mock_request_email()][0]
        except IndexError:
            bad_email = True
        assert bad_email == True

    # test negatif place

    def test_negatif_place(self):
        
        def mock_competition():
            return {'name': 'test', 'numberOfPlaces': -2}
            
        competition = mock_competition()
        result = negatif_place(competition)
        assert result == 0