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

#handle registration view
from app.forms import RegistrationForm

#handle last seen
from datetime import datetime,timezone

#Handle edit profile view
from app.forms import EditProfileForm

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


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

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username==username))
    posts=[
        {'author':user,'body':'test post #1'},
        {'author':user,'body':'test post #2'}
    ]
    return render_template('user.html',user=user,posts=posts)


@app.before_request
def before_request():
    #if current_user.is_authenticated:
     #   current_user.last_seen = datetime.now(timezone.utc)
      #  db.session.commit()
    pass
    #if current_user.is_authenticated:
        # Update the last_seen time to the current time on any request
     #   current_user.last_seen = datetime.now(timezone.utc)
      #  db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        now = datetime.now(timezone.utc)
        hour_str = now.strftime("%H")  # Extract hour as string
        minute_str = now.strftime("%M")  # Extract minute as string
        second_str = now.strftime("%S")  # Extract second as string

        # Convert the hour to an integer and add 6
        new_hour = (int(hour_str) + 6) % 24  # Use modulo 24 to handle overflow

        # Create the new time string
        new_time_str = f"{new_hour:02}:{minute_str}:{second_str}"

        # Combine with the current date
        new_datetime = now.replace(hour=new_hour)

        # Update the user's last seen time
        current_user.last_seen = new_datetime
        db.session.commit()
    logout_user()
    return redirect(url_for('index'))