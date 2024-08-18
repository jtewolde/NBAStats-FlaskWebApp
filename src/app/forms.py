"""
NBA Stats Web App
Developed by: Joseph Tewolde
Description: This is a web app that will display NBA stats for the 2023-2024 season.

"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    email_address = StringField('Email')
    about = TextAreaField('About')
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SignInForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')
