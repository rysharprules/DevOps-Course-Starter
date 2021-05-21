import json
from todo_app.Item import Item
from todo_app.Status import Status

class DatabaseMockHelper:

    statusesJson = './todo_app/mock/statuses.json'
    itemsJson = './todo_app/mock/items.json'

    def mockStatuses(self):
        statuses = []
        with open(self.statusesJson, 'r') as jsonFile:
            for data in json.load(jsonFile):
                statuses.append(Status(data['_id'], data['name']))
        return statuses

    def mockItems(self):
        items = []
        with open(self.itemsJson, 'r') as jsonFile:
            for data in json.load(jsonFile):
                item = Item(
                    data['_id'],
                    data['name'],
                    [status.title for status in self.mockStatuses() if data['status_ref']
                    == status.id][0],
                    data['desc'],
                    data['due'],
                    data['last_activity']
                )
                items.append(item)
        return items


    def mockData(self):
        return self.mockItems(), self.mockStatuses()
