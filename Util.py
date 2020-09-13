from Item import Item
from Status import Status
import requests
import sys


class Util:

    def __init__(self, base_uri, query, board_id):
        self.base_uri = base_uri
        self.query = query
        self.board_id = board_id

    def getApi(self, path):
        return requests.get(self.base_uri + path, params=self.query).json()

    def getStatuses(self):
        statuses = []
        for list in self.getApi(f'1/boards/{self.board_id}/lists'):
            status = Status(
                list['id'],
                list['name']
            )
            statuses.append(status)
        return statuses

    def getItemData(self):
        items = []
        statuses = self.getStatuses()
        for card in self.getApi(f'1/boards/{self.board_id}/cards'):
            item = Item(
                card['id'],
                card['name'],
                [status.title for status in statuses if card['idList'] == status.id][0],
                card['desc'],
                card['due'],
                card['dateLastActivity']
            )
            items.append(item)
        return items, statuses

    def getStatusIdForTitle(self, title):
        return [status.id for status in self.getStatuses() if status.title == title][0]

    def createItem(self, title, description="", due=""):
        query = self.query.copy()
        query['idList'] = self.getStatusIdForTitle('To Do')
        query['name'] = title
        query['desc'] = description
        query['due'] = due
        requests.post(self.base_uri + '1/cards', params=query)

    def updateItem(self, id, status):
        query = self.query.copy()
        query['idList'] = status
        requests.put(
            self.base_uri + f'1/cards/{id}',
            headers={"Accept": "application/json"},
            params=query
        )

    def removeItem(self, id):
        requests.delete(
            self.base_uri + f'1/cards/{id}', params=self.query)
