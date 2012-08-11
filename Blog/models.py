from Blog import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy(app)

"""
What should be the ideal design of the database of the blogging engine?
    1. If it's meant to be used by more than 1 user, must store user info.
    2. A second table containing all the posts, mapping with the respective users.
    3. The second table is the important one. What should be it's design? 
    4. Text format to store the blog posts.
    5. Associated metadata, like date and time of posting (displayed in localtime using pytz)
    6. Other stuff might be added in the future
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.Text)
    post_tags = db.Column(db.Text)
    post_on = db.Column(db.DateTime(timezone=pytz.timezone('UTC')))
