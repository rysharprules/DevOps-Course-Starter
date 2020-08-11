import requests
import sys
import os

API_KEY = os.environ.get("API_KEY", None)
API_TOKEN = os.environ.get("API_TOKEN", None)
BOARD_ID = os.environ.get("BOARD_ID", None)

BASE_URI = "https://api.trello.com/"
QUERY = {
    'key': API_KEY,
    'token': API_TOKEN
}

def getApi(path):
    uri = BASE_URI + path
    return requests.get(uri, params=QUERY).json()

def getStatuses():
    statuses = []
    for list in getApi(f'1/boards/{BOARD_ID}/lists'):
        status = {}
        status['id'] = list['id']
        status['title'] = list['name']
        statuses.append(status)
    return statuses

def getItemData():
    items = []
    statuses = getStatuses()
    for card in getApi(f'1/boards/{BOARD_ID}/cards'):
        item = {}
        item['id'] = card['id']
        item['title'] = card['name']
        item['status'] = [status['title']
                          for status in statuses if card['idList'] == status['id']][0]
        items.append(item)
    return items, statuses

def createItem(title):
    query = QUERY
    query['idList'] = getStatuses()[0]
    query['name'] = title
    requests.post(BASE_URI + '1/cards', params=query)

def updateItem(id, status):
    query = QUERY
    query['idList'] = status
    requests.put(
        BASE_URI + '1/cards/{}'.format(id),
        headers={"Accept": "application/json"},
        params=query
    )

def removeItem(id):
    requests.delete(BASE_URI + '1/cards/{}'.format(id), params=QUERY)
