from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
        util = current_app.config.get('util')
    util.board_id = util.create_trello_board('test_board')
    
    # start the app in its own thread
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # tear down
    thread.join(1)
    util.delete_trello_board(util.board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app):
    # load the page
    driver.get('http://localhost:5000/')
    # check title is available
    assert driver.title == 'To-Do App'

    # create an item
    title = driver.find_element_by_name('title')
    title.send_keys('test_item')
    driver.find_element_by_name("submit-item").submit()
    driver.implicitly_wait(2)
    item = driver.find_element_by_name('item-box')
    # check item is available
    assert item

    # move to doing
    item_id = item.get_attribute("id")
    source_element = driver.find_element_by_id(item_id)
    dest_element = driver.find_element_by_name('status-col-Doing')
    ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
    driver.implicitly_wait(2)
    # check item is available after drag and drop with correct class
    assert "bg-item" in driver.find_element_by_id(item_id).get_attribute("class")

    # complete the item
    complete_link = driver.find_element_by_name('item-complete-link')
    complete_link.click()
    driver.implicitly_wait(2)
    # check item is available after click complete with correct class
    assert "bg-complete" in driver.find_element_by_name(
        'item-box').get_attribute("class")

    # move back to do
    source_element = driver.find_element_by_id(item_id)
    dest_element = driver.find_element_by_name('status-col-To Do')
    ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
    driver.implicitly_wait(2)
    # check item is available after after drag and drop with complete link available again
    assert driver.find_element_by_name('item-complete-link')


    


    
