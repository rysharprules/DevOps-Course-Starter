from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import dotenv
import todo_app.app
from flask import current_app
from pathlib import Path
from todo_app.DatabaseHelper import DatabaseHelper
from todo_app.mock.DatabaseMockHelper import DatabaseMockHelper

mockHelper = DatabaseMockHelper()

@pytest.fixture(scope='module')
def test_app():
        dotenv.load_dotenv(dotenv.find_dotenv('.env.test'), override=True)
        application = todo_app.app.create_app()
        with application.app_context():
            application.config['api'] = DatabaseHelper
        
        # start the app in its own thread
        thread = Thread(target=lambda: application.run(use_reloader=False))
        thread.daemon = True
        thread.start()
        yield todo_app.app

        # tear down
        thread.join(1)

@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    opts.add_argument('--no-sandbox') 
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver


def test_task_journey(monkeypatch, driver, test_app):
    driver.implicitly_wait(3)
    global mockHelper
    monkeypatch.setattr(DatabaseHelper, 'getItemData', mockHelper.mockData)
    monkeypatch.setattr(DatabaseHelper, 'createItem', lambda a, b, c, d: None)

    # load the page
    driver.get('http://localhost:5000/')
    # check title is available
    assert driver.title == 'To-Do App'

    # create an item
    title = driver.find_element_by_name('title')
    title.send_keys('test_item')
    driver.find_element_by_name("submit-item").submit()
    item = driver.find_element_by_name('item-box')
    # check item is available
    assert item

    


    
