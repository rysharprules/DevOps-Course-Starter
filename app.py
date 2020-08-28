from flask import Flask, render_template, request, redirect, url_for
from api_items import getItemData, createItem, updateItem, removeItem, getStatusIdForTitle
from ViewModel import ViewModel
import sys

view_model = None

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        global view_model
        view_model = ViewModel(*getItemData())
        return render_template(
            'index.html',
            view_model=view_model
        )

    @app.route('/create', methods=['POST'])
    def create():
        createItem(request.form['title'], request.form['desc'], request.form['due'])
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

    @app.route('/toggle-done/<toggle>')
    def toggle_done(toggle):
        view_model.show_all_done_items = toggle == 'true'
        return render_template(
            'index.html',
            view_model=view_model
        )
    
    return app

if __name__ == '__main__':
    create_app().run()
