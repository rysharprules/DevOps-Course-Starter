from flask import Flask, render_template, request, redirect
from flask_login import login_required, login_user
from todo_app.ViewModel import ViewModel
from todo_app.DatabaseHelper import DatabaseHelper
from todo_app.User import User
from oauthlib.oauth2 import WebApplicationClient
import todo_app.login_manager as login_manager
import requests

viewModel = None

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.config['api'] = DatabaseHelper(app.config.get("DATABASE_URL"), app.config.get(
        "DATABASE_NAME"))
    api = app.config['api']
    login_manager.login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        global viewModel
        viewModel = ViewModel(*api.getItemData())
        return render_template(
            'index.html',
            viewModel=viewModel
        )

    @app.route('/create', methods=['POST'])
    @login_required
    def create():
        api.createItem(request.form['title'],
                       request.form['desc'], request.form['due'])
        return index()

    @app.route('/update', methods=['POST'])
    @login_required
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

    @app.route('/login/callback')
    def callback():
        client =  WebApplicationClient(app.config.get("CLIENT_ID"))
        token = client.prepare_token_request("https://github.com/login/oauth/access_token", code=request.args.get("code")) 
        access = requests.post(token[0], headers=token[1], data=token[2], auth=(app.config.get("CLIENT_ID"), app.config.get("CLIENT_SECRET")))
        client.parse_request_body_response(access.text)
        params = client.add_token("https://api.github.com/user")
        github_user = requests.get(params[0], headers=params[1]).json()
        login_user(User(github_user['id']))
        return redirect('/')
    
    return app

if __name__ == '__main__':
    create_app().run()
