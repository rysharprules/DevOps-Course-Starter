from flask import Flask, render_template, request, redirect, url_for
from api_items import getItemData, createItem, updateItem, removeItem, getStatusIdForTitle
import sys

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    items, statuses = getItemData()
    return render_template(
        'index.html',
        items=sorted(items, key=lambda item: item.status),
        statuses=statuses
    )

@app.route('/create', methods=['POST'])
def create():
    createItem(request.form['title'], request.form['desc'])
    return index()

@app.route('/update', methods=['POST'])
def update():
    updateItem(request.form['id'], request.form['status'])
    return index()

@app.route('/complete/<id>')
def complete_item(id):
    updateItem(id, getStatusIdForTitle('Done'))
    return index()

@app.route('/remove/<id>')
def remove(id):
    removeItem(id)
    return index()

if __name__ == '__main__':
    app.run()
