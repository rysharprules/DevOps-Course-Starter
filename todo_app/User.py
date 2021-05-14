from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = "writer" if id == "151856391" else "reader"