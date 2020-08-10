from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import requests
import sys

app = Flask(__name__)
app.config.from_object('flask_config.Config')

BOARD_ID = "NSn3rIEE"
BASE_URI = "https://api.trello.com/"
QUERY = {
   'key': '2caf651274e82aaad6db16b36a32631a',
   'token': 'd3fa3f8b7f9706afed48b78175d1c76239df1425d5334ea4ff0e170b508be9e6'
}

def getData(path):
    uri = BASE_URI + path
    return requests.get(uri, params=QUERY).json()

@app.route('/')
def index():
    cards = getData(f'1/boards/{BOARD_ID}/cards')
    lists = getData(f'1/boards/{BOARD_ID}/lists')
    statuses = []
    for list in lists:
        status = {}
        status['id'] = list['id']
        status['title'] = list['name']
        statuses.append(status)
    items = []
    for card in cards:
        item = {}
        item['id'] = card['id']
        item['title'] = card['name']
        item['status'] = [status['title'] for status in statuses if card['idList'] == status['id']][0]
        items.append(item)
    return render_template('index.html', items=items, statuses=statuses)

@app.route('/create', methods=['POST'])
def create():
    session.add_item(request.form['title'])
    return index()

@app.route('/update', methods=['POST'])
def update():
    for id in request.form:
        item = session.get_item(id)
        item['status'] = 'Complete'
        session.save_item(item)
    return index()

@app.route('/remove/<id>')
def remove(id):
    session.remove_item(id)
    return index()

if __name__ == '__main__':
    app.run()
