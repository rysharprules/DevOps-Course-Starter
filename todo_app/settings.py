import os

API_KEY = os.getenv("API_KEY")
API_TOKEN = os.getenv("API_TOKEN")
BOARD_ID = os.getenv("BOARD_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

BASE_URI = "https://api.trello.com/"
QUERY = {
    'key': API_KEY,
    'token': API_TOKEN
}
