# views.py
from flask import request, session, g, redirect, url_for, \
        abort, render_template, flash, jsonify, redirect

from flask import Flask

app = Flask(__name__)
app.config.from_envvar('BLOG_SETTINGS', silent=True)

def connect_db():
    pass

def init_db():
    pass
 
@app.route('/')
def index():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash("You were logged in!")
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

# This will be the main user dashboard used for adding and editing new posts.
@app.route('/dashboard')
def dashboard():
    pass

# Add new posts.
@app.route('/add', methods=['POST'])
def add():
    pass

# Remove an entry.
@app.route('/delete', methods=['POST'])
def remove():
    pass


@app.route('/logout')
def logout():
    pass

