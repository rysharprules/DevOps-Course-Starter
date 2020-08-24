import datetime

class Item:

    def getFormattedDueDate(self):
        hasDueDate, dueDate = self.getDueDate()
        if hasDueDate:
            return dueDate.strftime("%d/%m/%Y")
        return dueDate

    def isOverdue(self):
        hasDueDate, dueDate = self.getDueDate()
        if hasDueDate:
            return self.status != 'Done' and dueDate.date() <= datetime.date.today()
        return False

    def getDueDate(self):
        try:
            return True, datetime.datetime.strptime(self.due, '%Y-%m-%dT%H:%M:%S.%f%z')
        except (ValueError, TypeError) as e:
            return False, "No Due Date"

    def __init__(self, id, title, status, description, due):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.due = due
