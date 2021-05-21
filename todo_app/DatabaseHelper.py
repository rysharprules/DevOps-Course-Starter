from todo_app.Item import Item
from todo_app.Status import Status
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

class DatabaseHelper:

    def __init__(self, url, db):
        self._db = MongoClient(url)[db]

    def createItem(self, title, description="", due=""):
        item = {
            '_id': ObjectId(),
            'name': title,
            'desc': description,
            'due': due,
            'status_ref': self.getStatusIdForTitle('To Do'),
            'last_activity': self.getLastActivity()
        }
        self._db.items.insert_one(item)

    def getStatusIdForTitle(self, title):
        return [status.id for status in self.getStatuses() if status.title == title][0]

    def getLastActivity(self):
        return str(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def getStatuses(self):
        statuses = []
        for status in self._db.statuses.find():
            status = Status(
                str(status['_id']),
                status['name']
            )
            statuses.append(status)
        return statuses

    def getItems(self):
        return self._db.items.find()

    def getItemData(self):
        items = []
        statuses = self.getStatuses()
        for row in self.getItems():
            item = Item(
                row['_id'],
                row['name'],
                [status.title for status in statuses if row['status_ref'] == status.id][0],
                row['desc'],
                row['due'],
                row['last_activity']
            )
            items.append(item)
        return items, statuses

    def removeItem(self, id):
        self._db.items.delete_one({"_id": ObjectId(id)}) 

    def updateItem(self, id, statusId):
        item = {"$set": 
            {
                'status_ref': statusId,
                'last_activity': self.getLastActivity()
            }
        }
        self._db.items.update_one({"_id": ObjectId(id)}, item)
