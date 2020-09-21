from flask import Flask, render_template, request, redirect, url_for
from ViewModel import ViewModel
from ApiHelper import ApiHelper
import sys
import os

view_model = None

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.config['api'] = ApiHelper(app.config.get("BASE_URI"), app.config.get(
        "QUERY"), app.config.get("BOARD_ID"))
    api = app.config['api']

    @app.route('/')
    def index():
        global view_model
        view_model = ViewModel(*api.getItemData())
        return render_template(
            'index.html',
            view_model=view_model
        )

    @app.route('/create', methods=['POST'])
    def create():
        api.createItem(request.form['title'],
                       request.form['desc'], request.form['due'])
        return index()

    @app.route('/update', methods=['POST'])
    def update():
        api.updateItem(request.form['id'], request.form['status'])
        return index()

    @app.route('/complete/<id>')
    def complete_item(id):
        api.updateItem(id, api.getStatusIdForTitle('Done'))
        return index()

    @app.route('/remove/<id>')
    def remove(id):
        api.removeItem(id)
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
