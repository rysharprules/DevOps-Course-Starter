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
    # given
    monkeypatch.setattr(requests, "get", mock_get)

    # when
    response = client.get('/')

    # then
    assert response.status_code == 200
    assert "This task needs doing!" in str(response.data)

def test_create(monkeypatch, client):
    # given
    args = []
    test_title = 'test_title'
    test_desc = 'test_desc'
    test_due = 'test_due'
    test_status = 'test_todo_status'
    monkeypatch.setattr(requests, "post", lambda *a, **k: args.append(k['params']))
    monkeypatch.setattr(requests, "get", mock_get)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'title': test_title, 'desc': test_desc, 'due': test_due}

    # when
    response = client.post('/create', headers=headers, data=params)

    # then
    assert response.status_code == 200
    assert len(args[0]) == 6 # includes key and token
    assert args[0]['name'] == test_title
    assert args[0]['desc'] == test_desc
    assert args[0]['due'] == test_due
    assert args[0]['idList'] == test_status
    assert "This task needs doing!" in str(response.data)

def test_update(monkeypatch, client):
    # given
    args = []
    test_status = 'test_status'
    monkeypatch.setattr(requests, "put", lambda *a, **k: args.append(k['params']))
    monkeypatch.setattr(requests, "get", mock_get)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'id': 'test_id', 'status': test_status}

    # when
    response = client.post('/update', headers=headers, data=params)

    # then
    assert response.status_code == 200
    assert len(args[0]) == 3
    assert args[0]['idList'] == test_status
    assert "This task needs doing!" in str(response.data)

def test_complete_item(monkeypatch, client):
    # given
    args = []
    done_status = 'test_done_status'
    monkeypatch.setattr(requests, "put", lambda *a, **
                        k: args.append(k['params']))
    monkeypatch.setattr(requests, "get", mock_get)

    # when
    response = client.get('/complete/test_id')

    # then
    assert response.status_code == 200
    assert len(args[0]) == 3
    assert args[0]['idList'] == done_status
    assert "This task needs doing!" in str(response.data)

def test_remove(monkeypatch, client):
    # given
    args = []
    monkeypatch.setattr(requests, "delete", lambda *a, **
                        k: args.append(k['params']))
    monkeypatch.setattr(requests, "get", mock_get)

    # when
    response = client.get('/remove/test_id')

    # then
    assert response.status_code == 200
    assert len(args[0]) == 2
    assert "This task needs doing!" in str(response.data)

def test_toggle_done(monkeypatch, client):
    # given
    monkeypatch.setattr(requests, "get", mock_get)

    # when
    response = client.get('/')

    # then
    assert "An old done item" not in str(response.data)
    assert "Another old done item" not in str(response.data)
    assert "A third old done item" not in str(response.data)
    assert "A fourth old done item" not in str(response.data)
    assert "One last old done item" not in str(response.data)
    
    # when
    response = client.get('/toggle-done/true')

    # then
    assert "An old done item" in str(response.data)
    assert "Another old done item" in str(response.data)
    assert "A third old done item" in str(response.data)
    assert "A fourth old done item" in str(response.data)
    assert "One last old done item" in str(response.data)

    # when
    response = client.get('/toggle-done/false')

    # then
    assert "An old done item" not in str(response.data)
    assert "Another old done item" not in str(response.data)
    assert "A third old done item" not in str(response.data)
    assert "A fourth old done item" not in str(response.data)
    assert "One last old done item" not in str(response.data)
