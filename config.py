import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
    MAIL_SERVER = os.environ.get('smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('587') or 25)
    MAIL_USE_TLS = os.environ.get('1') is not None
    MAIL_USERNAME = os.environ.get('emonfashion555@gmail.com')
    MAIL_PASSWORD = os.environ.get('016CHEss')
    ADMINS = ['md.sazid.al.emon@gmail.com']
    POSTS_PER_PAGE = 25





#Package           Version
#----------------- -------
#alembic           1.13.2
#blinker           1.8.2
#click             8.1.7
#####Flask             3.0.3
#####Flask-Migrate     4.0.7
#####Flask-SQLAlchemy  3.1.1
#####Flask-WTF         1.2.1
#greenlet          3.0.3
#itsdangerous      2.2.0
#Jinja2            3.1.4
#Mako              1.3.5
#MarkupSafe        2.1.5
#pip               24.2
#####python-dotenv     1.0.1
#####SQLAlchemy        2.0.32
#typing_extensions 4.12.2
#Werkzeug          3.0.4
#####WTForms           3.1.2