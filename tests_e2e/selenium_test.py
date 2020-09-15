from threading import Thread
from selenium import webdriver
from Util import Util
import pytest
import dotenv
import app
from flask import current_app

@pytest.fixture(scope='module')
def test_app():
    dotenv.load_dotenv(dotenv.find_dotenv('.env'), override=True)
    application = app.create_app()
    util = None
    with application.app_context():
        util = Util(current_app.config.get("BASE_URI"),
                    current_app.config.get("QUERY"), '')
    board_id = util.create_trello_board('test_board')
    util.board_id = board_id
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # tear Down
    thread.join(1)
    util.delete_trello_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
