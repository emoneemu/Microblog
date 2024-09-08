from flask import Flask
from config import Config

#UTC time support
from flask_moment import Moment

#Email support
from flask_mail import Mail

#db state management
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Login state management
from flask_login import LoginManager


#Handling or Logging a rotating file
from logging.handlers import RotatingFileHandler,SMTPHandler
import os

#Log Errors by email
import logging
from logging.handlers import SMTPHandler

#Language Translator using flask babel extension
from flask import request
from flask_babel import Babel,_,lazy_gettext as _l


#Current app
from flask import current_app

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


#############################Base initialization#####################################
app = Flask(__name__)
#error handling
#from app import routes,models,errors

#error handle
from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

#UTC time support
moment = Moment()

app.config.from_object(Config)

#Language translator
babel = Babel()

#db-part
db = SQLAlchemy()
migrate = Migrate()

#Login-part
login = LoginManager()
login.login_view = 'auth.login'
#Language Translation
login.login_message = _l('Please log in to access this page.')

#Mail support
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

#Registering routes models errors etc python files
from app import models