'''Flask Web Application'''
from flask import Flask, render_template, flash, request, url_for, redirect, session, escape
from custom_form import RegistrationForm, LoginForm
from db_controller import SQLEngine
from db_model import User
from util import encrypt_password

# App config.
DEBUG = True
APP = Flask(__name__)
APP.config['SESSION_TYPE'] = 'memcached'
APP.config['SECRET_KEY'] = 'super secret key'

#Database Info
MYSQL_ENGINE = SQLEngine()

@APP.route('/')
def home():
    '''Home page'''
    if 'username' in session:
        flash('Logged in as %s' % escape(session['username']), 'info')
    return render_template('index.html')


@APP.route('/login', methods=['GET', 'POST'])
def login():
    '''Login page'''
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        is_login_success = MYSQL_ENGINE.check_login(
            form.username.data,
            form.password.data)
        if is_login_success:
            flash('Login successful!', 'success')
            session['username'] = form.username.data
        else:
            flash('Username/password is incorrect! Please try again or sign up.', 'warning')
        form.clean()
    return render_template('login-form.html', form=form)


@APP.route('/register', methods=['GET', 'POST'])
def register():
    '''Registration page'''
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        form.password.data = encrypt_password(form.password.data)
        is_registration_success = MYSQL_ENGINE.add_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
            )
        if is_registration_success:
            flash('Thanks for registration ' + str(form.username.data), 'info')
        else:
            flash('Your data existed in the system, please login.', 'warning')
        form.clean()
    return render_template('registration-form.html', form=form)


if __name__ == "__main__":
    APP.run()
