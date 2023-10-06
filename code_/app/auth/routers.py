from flask import Blueprint, render_template, Request, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.database import db
from flask_login import login_user, logout_user

from app.models import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('auth/login.html')
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('word.list_words'))


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('auth/login.html')
        # return render_template('auth/signup.html')
    # # code to validate and add user to database goes here
    # email = request.form.get('email')
    # name = request.form.get('name')
    # password = request.form.get('password')
    #
    # user = User.query.filter_by(
    #     email=email).first()  # if this returns a user, then the email already exists in database
    #
    # if user:  # if a user is found, we want to redirect back to signup page so user can try again
    #     return redirect(url_for('auth.signup'))
    #
    # # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    #
    # # add the new user to the database
    # db.session.add(new_user)
    # db.session.commit()

    return redirect(url_for('auth.login'))


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
