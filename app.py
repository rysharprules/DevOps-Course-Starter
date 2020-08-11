from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import session_items as session
import requests
import sys
import os

app = Flask(__name__)
app.config.from_object('flask_config.Config')

API_KEY = os.environ.get("API_KEY", None)
API_TOKEN = os.environ.get("API_TOKEN", None)

BOARD_ID = "NSn3rIEE"
BASE_URI = "https://api.trello.com/"
QUERY = {
    'key': API_KEY,
    'token': API_TOKEN
}

def getApi(path):
    uri = BASE_URI + path
    return requests.get(uri, params=QUERY).json()

def getStatuses():
    statuses = []
    for list in getApi(f'1/boards/{BOARD_ID}/lists'):
        status = {}
        status['id'] = list['id']
        status['title'] = list['name']
        status['initial'] = list['name'] == 'To Do'
        statuses.append(status)
    return statuses

def getData():
    items = []
    statuses = getStatuses()
    for card in getApi(f'1/boards/{BOARD_ID}/cards'):
        item = {}
        item['id'] = card['id']
        item['title'] = card['name']
        item['status'] = [status['title']
                          for status in statuses if card['idList'] == status['id']][0]
        items.append(item)
    return items, statuses

@app.route('/')
def index():
    items, statuses = getData()
    return render_template('index.html', items=items, statuses=statuses)

@app.route('/create', methods=['POST'])
def create():
    uri = BASE_URI + '1/cards'
    query = QUERY
    query['idList'] = [status['id'] for status in getStatuses() if status['initial']][0]
    query['name'] = request.form['title']
    requests.post(uri, params=query)
    return index()

@app.route('/update', methods=['POST'])
def update():
    uri = BASE_URI + '1/cards/{}'.format(request.form['id'])
    headers = {
        "Accept": "application/json"
    }
    query = QUERY
    query['idList'] = request.form['status']
    requests.put(
        uri,
        headers=headers,
        params=query
    )
    return index()

@app.route('/remove/<id>')
def remove(id):
    uri = BASE_URI + '1/cards/{}'.format(id)
    requests.delete(uri, params=QUERY)
    return index()

if __name__ == '__main__':
    app.run()
