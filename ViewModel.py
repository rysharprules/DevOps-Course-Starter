from datetime import *

class ViewModel:

    board_statuses = ["To Do", "Doing", "Done"]

    def __init__(self, items, statuses):
        self._items = items
        self._statuses = statuses
        self._show_all_done_items = False

    @property
    def items(self):
        return self._items

    @property
    def statuses(self):
        return self._statuses

    @property
    def show_all_done_items(self):
        return self._show_all_done_items

    @show_all_done_items.setter
    def show_all_done_items(self, value):
        self._show_all_done_items = value

    def getBoardStatuses(self):
        return [status for status in self.statuses if status.title in ViewModel.board_statuses]

    def getToDoItems(self):
        return self.filterItemsByStatus(self.getStatusWithTitle(ViewModel.board_statuses[0]))

    def getDoingItems(self):
        return self.filterItemsByStatus(self.getStatusWithTitle(ViewModel.board_statuses[1]))

    def getDoneItems(self):
        allDoneItems = self.getAllDoneItems()
        if len(allDoneItems) < 5 or self.show_all_done_items:
            return allDoneItems
        return self.filterItemsByDoneDate(allDoneItems, date.today())

    def getAllDoneItems(self):
        return self.filterItemsByStatus(self.getStatusWithTitle(ViewModel.board_statuses[2]))

    def getStatusWithTitle(self, title):
        return [status for status in self.statuses if status.title == title][0]

    def filterItemsByDoneDate(self, items, doneDate):
        return [item for item in items if date(int(item.done[:4]), int(item.done[5:7]), int(item.done[8:10])) == doneDate]

    def filterItemsByStatus(self, status):
        return [item for item in self.items if item.status == status.title]
