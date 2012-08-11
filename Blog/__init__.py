from flask import Flask
app = Flask(__name__)
app.config.from_envvar('BLOG_SETTINGS')

import Blog.views
