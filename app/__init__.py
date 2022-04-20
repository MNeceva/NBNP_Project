from flask import Flask

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig") # argument is file_name.class_of_the_config_you_want_to_run
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
    

from flask_mongoengine import MongoEngine
db = MongoEngine(app)

from flask_mail import Mail
mail = Mail(app)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .auth import auth as auth_blueprint
from .main import main as main_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')

app.register_blueprint(main_blueprint, url_prefix='/main')

from app import views
from app import models
from app import forms



