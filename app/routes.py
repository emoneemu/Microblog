from flask import render_template,flash,redirect,url_for
from app import app,db

#handle split url
from flask import request
from urllib.parse import urlsplit
#handle forms
from app.forms import LoginForm

#handle db
import sqlalchemy as sa;
from app.models import User

#handle login-logout view
from flask_login import current_user,login_user,logout_user,login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    #return "Hello, World!"
    #user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
           'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title='Home Page',posts=posts)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        #we no longer need the flash system as we integrated with db
        #flash('Login requested for user {}, remember_me={}'.format(
            #form.username.data, form.remember_me.data))
        user=db.session.scalar(
            sa.select(User).where(User.username ==form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc !='':
            next_page=url_for('index')
        #return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html',title='Sign In',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))