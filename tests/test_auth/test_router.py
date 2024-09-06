import pytest


@pytest.mark.usefixtures('recreate_tables',)
class TestRouter:
    def test_access_token_auth(self, client, random_user):
        username, password, user = random_user
        data = dict(username=username, password=password)
        response = client.post('auth/token', data=data)

        assert response.status_code == 200
        token_data = response.json()
        assert token_data['access_token']
        assert token_data['token_type'] == 'bearer'

    def test_access_token_not_auth(self, client):
        data = dict(username='some@email.com', password='invalid')
        response = client.post('auth/token', data=data)

        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_read_user_auth(self, client, random_user):
        username, password, user = random_user
        data = dict(username=username, password=password)
        auth_token = client.post('/auth/token', data=data).json()['access_token']
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('auth/users/me', headers=headers)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['email'] == username
        assert response_data['role'] == 'USER'
        assert response_data['state'] == 'ACTIVE'

    def test_read_user_invalid_token(self, client):
        headers = {'Authorization': 'Bearer some_wrong_token'}
        response = client.get('/auth/users/me', headers=headers)

        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}

    def test_read_user_not_auth(self, client):
        response = client.get('/auth/users/me')

        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
