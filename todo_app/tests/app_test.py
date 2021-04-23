import pytest
import dotenv
import todo_app.app
import json
from todo_app.Item import Item
from todo_app.Status import Status
from todo_app.DatabaseHelper import DatabaseHelper

statusesJson = './todo_app/tests/mock/statuses.json'
itemsJson = './todo_app/tests/mock/items.json'
mockTodo = "Buy recycled mango scented candles"

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('../.env.test')
    dotenv.load_dotenv(file_path, override=True)
    application = todo_app.app.create_app()
    with application.test_client() as client:
        yield client
    application.config['api'] = DatabaseHelper

def mockStatuses():
    statuses = []
    with open(statusesJson, 'r') as jsonFile:
        for data in json.load(jsonFile):
            statuses.append(Status(data['_id'], data['name']))
    return statuses

def mockItems():
    items = []
    with open(itemsJson, 'r') as jsonFile:
        for data in json.load(jsonFile):
            item = Item(
                data['_id'],
                data['name'],
                [status.title for status in mockStatuses() if data['status_ref']
                 == status.id][0],
                data['desc'],
                data['due'],
                data['last_activity']
            )
            items.append(item)
    return items

def mockData(self):
    return mockItems(), mockStatuses()

def testIndex(monkeypatch, client):
    monkeypatch.setattr(DatabaseHelper, 'getItemData', mockData)
    assert mockTodo in client.get('/').data.decode()
