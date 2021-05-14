from flask_login import LoginManager
from flask import redirect, current_app as app
from oauthlib.oauth2 import WebApplicationClient

login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    client =  WebApplicationClient(app.config.get("CLIENT_ID"))
    return redirect(client.prepare_request_uri("https://github.com/login/oauth/authorize")) 

@login_manager.user_loader
def load_user(user_id):
    return None

login_manager.init_app(app)