import datetime

class Item:

    def parseDue(self, due):
        dueFormatted = "No Due Date"
        overdue = False
        if due:
            dueDate = datetime.datetime.strptime(due, '%Y-%m-%dT%H:%M:%S.%f%z')
            dueFormatted = dueDate.strftime("%d/%m/%Y")
            overdue = self.status != 'Done' and dueDate.date() <= datetime.date.today()
        return dueFormatted, overdue

    def __init__(self, id, title, status, description="", due=""):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.dueFormatted, self.overdue = self.parseDue(due)