import requests

api_url = 'http://localhost:8000'

def test_healthcheck():
    response = requests.get(f'{api_url}/__health')
    assert response.status_code == 200

class TestMusics():
    def test_get_empty_music(self):
        response = requests.get(f'{api_url}/v1/musics')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_add_music(self):
        body = { "title": "New music", "name": "name music" }
        response = requests.post(f'{api_url}/v1/musics', json = body)
        assert response.status_code == 200
        assert response.json().get('title') == 'New music'
        assert response.json().get('name') == 'name music'
        assert response.json().get('id') == 0

    def get_musics_by_id(self):
        response = requests.get(f'{api_url}/v1/musics/0')
        assert response.status_code == 200
        assert response.json().get('title') == 'New music'
        assert response.json().get('name') == 'name music'
        assert response.json().get('id') == 0

    def test_get_not_empty_music(self):
        response = requests.get(f'{api_url}/v1/musics')
        assert response.status_code == 200
        assert len(response.json()) == 1