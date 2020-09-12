import pytest
import dotenv
import app
import requests
import json

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
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

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, "get", mock_get)

    response = client.get('/')
    assert response.status_code == 200
    assert "Buy recycled mango scented candles" in str(response.data)
    assert "Calmly collaborate and agree on an effective plan of action" in str(
        response.data)
