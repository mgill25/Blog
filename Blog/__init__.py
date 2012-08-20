from flask import Flask
app = Flask(__name__)
app.config.from_envvar('BLOG_SETTINGS')


# This should always be the last statement!
import Blog.views
