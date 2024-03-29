from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from configs.config import Config


app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = "login"
bootstrap = Bootstrap(app)