class ViewModel:

    board_statuses = ["To Do", "Doing", "Done"]

    def __init__(self, items, statuses):
        self._items = items
        self._statuses = statuses

    @property
    def items(self):
        return self._items

    @property
    def statuses(self):
        return self._statuses

    def getBoardStatuses(self):
        return [status for status in self.statuses if status.title in ViewModel.board_statuses]

    def getToDoItems(self):
        return self.filterItemsByStatus(self.getStatusWithTitle(ViewModel.board_statuses[0]))

    def getDoingItems(self):
        return self.filterItemsByStatus(self.getStatusWithTitle(ViewModel.board_statuses[1]))

    def getDoneItems(self):
        return self.filterItemsByStatus(self.getStatusWithTitle(ViewModel.board_statuses[2]))

    def getStatusWithTitle(self, title):
        return [status for status in self.statuses if status.title == title][0]

    def filterItemsByStatus(self, status):
        return [item for item in self.items if item.status == status.title]
