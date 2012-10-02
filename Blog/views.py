# views.py
from flask import request, session, g, redirect, url_for, \
        abort, render_template, flash, jsonify, redirect, Response
from Blog import app
from Blog.models import db, User, Post, Category
from flaskext.bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
import re
from functools import wraps

def create_user(username, email, password):
    """Takes a bcrypt object for password encoding."""
    password_hash = generate_password_hash(password, rounds=10)
    try:
        new_user = User(username=username, email=email, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        app.logger.debug('%s - %s' %(type(e), str(e)))

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['USERNAME'] and password == app.config['PASSWORD']

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

"""
def create_post(title, body, draft, category, post_on):
    try:
        new_post = Post(title=title, body=body, draft=draft, category=category, post_on=post_on)
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        app.logger.debug('%s - %s' %(type(e), str(e)))
"""

@app.route('/')
def index():
    """Show recent posts on the main page, starting from most recent."""
    try:
        posts = Post.query.filter_by(draft=False).all()  # all the non-draft posts.
        #print posts
        return render_template('index.html', posts=posts)
    except Exception as e:
        app.logger.debug('%s - %s' %(type(e), str(e)))
        #abort(404)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# This will be the main user dashboard used for adding and editing new posts.
@app.route('/dashboard', methods=['GET', 'POST'])
@requires_auth
def dashboard():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash("You were logged in!")
            return render_template('dashboard.html')
    if error != None:
        app.logger.debug(error)
    return render_template('dashboard.html', error=error)

# Add new posts.
@app.route('/add', methods=['POST'])
@requires_auth
def add():
    # app.logger.debug(request.form)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['text']
        pattern = re.compile(r'\n')
        body = re.sub(pattern, '<br />', body)
        draft = True if request.form.has_key('draft') else False   # don't show drafts on the index page
        category = Category(request.form['category']) if request.form.has_key('category') else 'default'
        post_on = datetime.now()
        form_data = Post(title,body,draft,category,post_on)
        db.session.add(form_data)
        db.session.commit()
    else:
        app.logger.error('Invalid method!')
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
@requires_auth
def delete():
    """Permanently remove the given post from the database"""
    app.logger.debug(request.form['id'])
    post = Post.query.filter_by(id=request.form['id'])
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted!");
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You were logged out!")
    return redirect(url_for('index'))

@app.route('/drafts')
@requires_auth
def drafts():
    """Query the posts where the draft field is set to True"""
    try:
        posts = Post.query.filter_by(draft=True).all()
        return render_template('drafts.html', posts=posts)
    except Exception as e:
        app.logger.debug('%s - %s' %(type(e), str(e)))

