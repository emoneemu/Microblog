#for user table
from typing import Optional

#for password hasing method implement
from werkzeug.security import generate_password_hash,check_password_hash

#for db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

#for post
from datetime import datetime,timezone

#For login credential Using Mixin generic class
from flask_login import UserMixin

#For user loader
from app import login

#user table class,here UserMixin is for login credential
class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
#blog post table class
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    


#Needs a user loader function , because flask-login knows nothing about db. Because Flask-Login knows nothing about databases, 
#it needs the application's help in loading a user. For that reason, the extension expects that the application will configure
# a user loader function, that can be called to load a user given the ID.

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))