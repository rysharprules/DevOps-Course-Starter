from flask_login import UserMixin

class User(UserMixin):

    writer = "writer"
    reader = "reader"

    def __init__(self, id):
        self.id = id
        self.role = User.writer if id == "15185639" else User.reader

    @property
    def isWriter(self):
        return self.role == User.writer