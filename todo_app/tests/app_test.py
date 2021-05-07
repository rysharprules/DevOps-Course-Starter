import pytest
import dotenv
import todo_app.app
from todo_app.DatabaseHelper import DatabaseHelper
from todo_app.mock.DatabaseMockHelper import DatabaseMockHelper

mockTodo = "Buy recycled mango scented candles"
mockHelper = DatabaseMockHelper()

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('../.env.test')
    dotenv.load_dotenv(file_path, override=True)
    application = todo_app.app.create_app()
    with application.test_client() as client:
        yield client
    application.config['api'] = DatabaseHelper

def testIndex(monkeypatch, client):
    monkeypatch.setattr(DatabaseHelper, 'getItemData', mockHelper.mockData)
    assert mockTodo in str(client.get('/').data)

def testCreate(monkeypatch, client):
    # given
    test_title = 'test_title'
    test_desc = 'test_desc'
    test_due = 'test_due'
    monkeypatch.setattr(DatabaseHelper, 'getItemData', mockHelper.mockData)
    monkeypatch.setattr(DatabaseHelper, 'createItem', lambda a,b,c,d: None)

    # when
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'title': test_title, 'desc': test_desc, 'due': test_due}
    response = client.post('/create', headers=headers, data=params)

    # then
    assert response.status_code == 200
    assert mockTodo in str(response.data)


def testUpdate(monkeypatch, client):
    # given
    test_status = 'test_status'
    monkeypatch.setattr(DatabaseHelper, 'getItemData', mockHelper.mockData)
    monkeypatch.setattr(DatabaseHelper, 'updateItem', lambda a,b,c: None)

    # when
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'id': 'test_id', 'status': test_status}
    response = client.post('/update', headers=headers, data=params)

    # then
    assert response.status_code == 200
    assert mockTodo in str(response.data)


def testRemove(monkeypatch, client):
    # given
    monkeypatch.setattr(DatabaseHelper, 'getItemData', mockHelper.mockData)
    monkeypatch.setattr(DatabaseHelper, 'removeItem', lambda a,b: None)

    # when
    response = client.get('/remove/test_id')

    # then
    assert response.status_code == 200
    assert mockTodo in str(response.data)
