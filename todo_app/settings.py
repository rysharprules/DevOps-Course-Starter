import os

API_KEY = os.getenv("API_KEY")
API_TOKEN = os.getenv("API_TOKEN")
BOARD_ID = os.getenv("BOARD_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
LOGIN_DISABLED = os.getenv("LOGIN_DISABLED")

BASE_URI = "https://api.trello.com/"
QUERY = {
    'key': API_KEY,
    'token': API_TOKEN
}
