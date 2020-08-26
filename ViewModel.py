class ViewModel:

    def __init__(self, items, statuses):
        self._items = items
        self._statuses = statuses

    @property
    def items(self):
        return self._items

    @property
    def statuses(self):
        return self._statuses
