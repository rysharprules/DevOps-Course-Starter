import pytest
import dotenv
import app
import requests
import json

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


class MockStatusResponse:

    @staticmethod
    def json():
        with open('tests/mock/statuses.json', 'r') as json_file:
            return json.load(json_file)


class MockItemResponse:

    @staticmethod
    def json():
        with open('tests/mock/items.json', 'r') as json_file:
            return json.load(json_file)


def mock_get(*args, **kwargs):
    if "lists" in args[0]:
        return MockStatusResponse()
    else:  # elif "cards" in args[0]:
        return MockItemResponse()

def test_index(monkeypatch, client):
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get('/')

    assert response.status_code == 200
    assert "Buy recycled mango scented candles" in str(response.data)
    assert "Calmly collaborate and agree on an effective plan of action" in str(
        response.data)


def test_create(monkeypatch, client):
    args = []
    test_title = 'test_title'
    test_desc = 'test_desc'
    test_due = 'test_due'
    test_status = 'test_todo_status'
    monkeypatch.setattr(requests, "post", lambda *a, **k: args.append(k['params']))
    monkeypatch.setattr(requests, "get", mock_get)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'title': test_title, 'desc': test_desc, 'due': test_due}
    response = client.post('/create', headers=headers, data=params)

    assert response.status_code == 200
    assert len(args[0]) == 6 # includes key and token
    assert args[0]['name'] == test_title
    assert args[0]['desc'] == test_desc
    assert args[0]['due'] == test_due
    assert args[0]['idList'] == test_status
