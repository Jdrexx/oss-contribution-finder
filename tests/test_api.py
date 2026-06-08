from fastapi.testclient import TestClient
from src.main import app
client = TestClient(app)
def test_health():
    r=client.get('/api/health')
    assert r.status_code == 200
    assert r.json()['ok'] is True

def test_search_mock():
    data=client.post('/api/search', json={'skills':'Python','language':'python','difficulty':'any'}).json()
    assert 'count' in data
