'''Custom Form Class - Module'''
from wtforms import TextField, PasswordField, Form
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
class RegistrationForm(Form):
    '''
    Registration Form
    Username - Email - Password - Confirm Password
    '''
    username = TextField("Username", validators=[
        InputRequired('Please enter your name.')])
    email = EmailField("Email", validators=[
        InputRequired("Please enter your email address."),
        Email("Invalid email.")])
    password = PasswordField('New Password', validators=[
        DataRequired("Please enter your password."),
        EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    def clean(self):
        '''Clean data for form'''
        self.username.data = None
        self.email.data = None
        self.password.data = None
        self.confirm.data = None

class LoginForm(Form):
    '''
    Login Form
    Username - Password
    '''
    username = TextField("Username", validators=[
        InputRequired('Please enter your name.')])
    password = PasswordField('Password', validators=[
        DataRequired("Please enter your password.")])

    def clean(self):
        '''Clean data for form'''
        self.username.data = None
        self.password.data = None
