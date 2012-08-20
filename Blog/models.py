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
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(40))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' %self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text, default="")
    draft = db.Column(db.Boolean(), index=True, default=True)
    post_on = db.Column(db.DateTime(timezone=pytz.timezone('UTC')))
    updated_on = db.Column(db.DateTime(timezone=pytz.timezone('UTC')))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref= db.backref('posts',lazy='dynamic'))

    def __init__(self, title, body, draft=False, category=None, post_on=None):
        self.title = title
        self.body = body
        self.draft = draft
        if post_on is None:
            post_on = datetime.utcnow()
        self.post_on = post_on
        self.category = category

    def update_post(updated_on=None):
        if updated_on is not None:
            self.updated_on = updated_on

    def __repr__(self):
        return '<Post %r>' %self.title

# Instead of having a 'tags' column in the posts, we can define categories seperately,
# this way, we can easily query all the posts associated with a certain category.
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' %self.name

# Create the database
try:
    db.create_all()
except Exception as e:
    app.logger.debug("%s - %s" %(type(e), str(e)))
