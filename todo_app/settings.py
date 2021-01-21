from os import environ

API_KEY = environ.get("API_KEY", None)
API_TOKEN = environ.get("API_TOKEN", None)
BOARD_ID = environ.get("BOARD_ID", None)

BASE_URI = "https://api.trello.com/"
QUERY = {
    'key': API_KEY,
    'token': API_TOKEN
}
