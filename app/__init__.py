from flask import Flask
from config import Config

#db state management
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Login state management
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

#db-part
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Login-part
login = LoginManager(app)
login.login_view = 'login'
from app import routes,models