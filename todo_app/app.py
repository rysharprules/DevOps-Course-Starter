from flask import Flask, render_template, request
from todo_app.ViewModel import ViewModel
from todo_app.DatabaseHelper import DatabaseHelper

viewModel = None

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.config['api'] = DatabaseHelper(app.config.get("DATABASE_URL"), app.config.get(
        "DATABASE_NAME"))
    api = app.config['api']

    @app.route('/')
    def index():
        global viewModel
        viewModel = ViewModel(*api.getItemData())
        return render_template(
            'index.html',
            viewModel=viewModel
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
    def completeItem(id):
        api.updateItem(id, api.getStatusIdForTitle('Done'))
        return index()

    @app.route('/remove/<id>')
    def remove(id):
        api.removeItem(id)
        return index()

    @app.route('/toggle-done/<toggle>')
    def toggleDone(toggle):
        viewModel.show_all_done_items = toggle == 'true'
        return render_template(
            'index.html',
            viewModel=viewModel
        )
    
    return app

if __name__ == '__main__':
    create_app().run()
