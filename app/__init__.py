from flask import Flask
from flask_bootstrap import Bootstrap
#from flask_login import LoginManager

app = Flask(__name__)
app.config.update(
    SECRET_KEY='SECRET_KEY-cahuet')

#login = LoginManager(app)

#bootstrap = Bootstrap(app)
from app import routes

