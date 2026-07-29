from fastapi.testclient import TestClient
from src.main import app
client = TestClient(app)
def test_health():
    r=client.get('/api/health')
    assert r.status_code == 200
    assert r.json()['ok'] is True

class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self):
        import json

        return json.dumps(self.payload).encode()


def test_search_mock(monkeypatch):
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *args, **kwargs: FakeResponse({"items": []}),
    )
    data=client.post('/api/search', json={'skills':'Python','language':'python','difficulty':'any'}).json()
    assert 'count' in data


def test_search_rejects_query_injection():
    response = client.post(
        "/api/search",
        json={"skills": "python", "language": "python state:closed", "difficulty": "any"},
    )

    assert response.status_code == 422


def test_search_rejects_unknown_difficulty():
    response = client.post(
        "/api/search",
        json={"skills": "python", "language": "python", "difficulty": "impossible"},
    )

    assert response.status_code == 422
