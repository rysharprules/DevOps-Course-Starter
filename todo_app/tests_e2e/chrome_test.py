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
import mongomock

mockHelper = DatabaseMockHelper()

@pytest.fixture(scope='module')
def test_app():
    with mongomock.patch(servers=('mongodb://server.example.com:27017',)):
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
    monkeypatch.setattr(DatabaseHelper, 'getItemData', mockHelper.mockData)
    monkeypatch.setattr(DatabaseHelper, 'createItem', lambda a, b, c, d: None)
    monkeypatch.setattr(DatabaseHelper, 'updateItem', lambda a, b, c: None)
    monkeypatch.setattr(DatabaseHelper, 'removeItem', lambda a, b: None)

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

    # move to doing
    item_id = item.get_attribute("id")
    source_element = driver.find_element_by_id(item_id)
    dest_element = driver.find_element_by_name('status-col-Doing')
    ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
    # check item is available after drag and drop with correct class
    # assert "bg-item" in driver.find_element_by_id(item_id).get_attribute("class")

    # # complete the item
    # complete_link = driver.find_element_by_name('item-complete-link')
    # complete_link.click()
    # # check item is available after click complete with correct class
    # assert "bg-complete" in driver.find_element_by_name(
    #     'item-box').get_attribute("class")

    # # move back to do
    # source_element = driver.find_element_by_id(item_id)
    # dest_element = driver.find_element_by_name('status-col-To Do')
    # ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
    # # check item is available after after drag and drop with complete link available again
    # assert driver.find_element_by_name('item-complete-link')


    


    
