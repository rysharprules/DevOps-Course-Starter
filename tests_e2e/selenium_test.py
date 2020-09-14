import os
from threading import Thread
import app
import requests
from selenium import webdriver

@pytest.fixture(scope='module')
def test_app():
    # construct the new application
    application = app.create_app()
    # Create the new board & update the board id environment variable
    board_id = app.util.create_trello_board()
    os.environ['BOARD_ID'] = board_id
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    app.util.delete_trello_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
