from Item import Item
from Status import Status
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
    return requests.get(BASE_URI + path, params=QUERY).json()

def getStatuses():
    statuses = []
    for list in getApi(f'1/boards/{BOARD_ID}/lists'):
        status = Status(
            list['id'],
            list['name']
        )
        statuses.append(status)
    return statuses

def getItemData():
    items = []
    statuses = getStatuses()
    for card in getApi(f'1/boards/{BOARD_ID}/cards'):
        item = Item(
            card['id'],
            card['name'],
            [status.title for status in statuses if card['idList'] == status.id][0],
            card['desc']
        )
        items.append(item)
    return items, statuses

def getStatusIdForTitle(title):
    return [status.id for status in getStatuses() if status.title == title][0]

def createItem(title, description=""):
    query = QUERY
    query['idList'] = getStatuses()[0].id
    query['name'] = title
    query['desc'] = description
    requests.post(BASE_URI + '1/cards', params=query)

def updateItem(id, status):
    query = QUERY
    query['idList'] = status
    requests.put(
        BASE_URI + f'1/cards/{id}',
        headers={"Accept": "application/json"},
        params=query
    )

def removeItem(id):
    requests.delete(BASE_URI + f'1/cards/{id}', params=QUERY)
