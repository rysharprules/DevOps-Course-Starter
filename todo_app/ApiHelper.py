from todo_app.Item import Item
from todo_app.Status import Status
import requests
import sys


class ApiHelper:

    def __init__(self, base_uri, query, board_id):
        self._base_uri = base_uri
        self._query = query
        self._board_id = board_id

    @property
    def board_id(self):
        return self._board_id

    @board_id.setter
    def board_id(self, value):
        self._board_id = value

    def getApi(self, path):
        return requests.get(self._base_uri + path, params=self._query).json()

    def getStatuses(self):
        statuses = []
        for list in self.getApi(f'1/boards/{self._board_id}/lists'):
            status = Status(
                list['id'],
                list['name']
            )
            statuses.append(status)
        return statuses

    def getItemData(self):
        items = []
        statuses = self.getStatuses()
        for card in self.getApi(f'1/boards/{self._board_id}/cards'):
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
        query = self._query.copy()
        query['idList'] = self.getStatusIdForTitle('To Do')
        query['name'] = title
        query['desc'] = description
        query['due'] = due
        requests.post(self._base_uri + '1/cards', params=query)

    def updateItem(self, id, status):
        query = self._query.copy()
        query['idList'] = status
        requests.put(
            self._base_uri + f'1/cards/{id}',
            headers={"Accept": "application/json"},
            params=query
        )

    def removeItem(self, id):
        requests.delete(
            self._base_uri + f'1/cards/{id}', params=self._query)

    def create_trello_board(self, name):
        query = self._query.copy()
        query['name'] = name
        return requests.post(self._base_uri + '1/boards', params=query).json()['id']

    def delete_trello_board(self, board_id):
        requests.delete(self._base_uri + f'1/boards/{board_id}', params=self._query)
