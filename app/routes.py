from app import app, db, load_user
from app.models import User
from app.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt, uuid
from app.api import get_teams, get_players, get_player_total_stats, get_player_avg_stats

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    """ This route handles the signin process, authenticating the user and redirecting the user to the orders page. """
    form = SignInForm() # instantiate a signin form
    if form.validate_on_submit(): 
        user = User.query.filter_by(id=form.id.data).first() # check if the user exists using the id
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd): # if the user exists and the password matches
            login_user(user) # login the user
            return redirect(url_for('teams')) # redirect the user to the orders page
        else:
            return '<p>Sorry, the user id and/or password are incorrect!</p>' # print an error message
    return render_template('signin.html', form=form) # render the signin template if the form was not submitted or it is not valid

@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    """ This route handles the signup process, creating a new user and storing it in the local database,
        and then redirecting the user to the signin page, and create a Square customer for the user. """
    form = SignUpForm() # instantiate a signup form
    if form.validate_on_submit(): # if the form was submitted and it is valid
        existing_user = User.query.filter_by(id=form.id.data).first() # check if the user already exists using the id
        if existing_user: # if the user already exists
            return '<p>Sorry, this user id is already taken!</p>' # print an error message

        passwd = form.passwd.data # get the password from the form
        passwd_confirm = form.passwd_confirm.data # get the password confirmation from the form

        if passwd == passwd_confirm: # if the password and the password confirmation match
            salt_passwd = bcrypt.gensalt() # generate a salt
            hashed_passwd = bcrypt.hashpw(passwd.encode('utf-8'), salt_passwd) # hash the password using the salt

            # create a new user 
            new_user = User(id=form.id.data, email_address = form.email_address.data, about = form.about.data, passwd=hashed_passwd) # instantiate a new user with the id, customer_id, and hashed password
            db.session.add(new_user) # add the new user to the database
            db.session.commit() # commit the changese

            return redirect(url_for('users_signin')) # redirect the user to the signin page
        else: # if the password and the password confirmation do not match
            return '<p>Sorry, the password and the password confirmation do not match!</p>'
    return render_template('signup.html', form=form) # render the signup template if the form was not submitted or it is not valid

    
@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    """This route handles the signout process, logging out the user and redirecting the user to the index page."""
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/teams', methods=['GET', 'POST'])
def teams():
    """This route handles the teams page, displaying all NBA teams."""
    return render_template('teams.html', teams=get_teams())
