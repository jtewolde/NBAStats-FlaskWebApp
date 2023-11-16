"""
NBA Stats Web App
Developed by: Joseph Tewolde
Description: This is a web app that will display NBA stats for the 2023-2024 season.

"""

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email_address = db.Column(db.String)
    about = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)