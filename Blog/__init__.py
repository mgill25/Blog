from flask import Flask
app = Flask(__name__)
app.config.from_envvar('BLOG_SETTINGS')

# Register a jijna filter.
app.jinja_env.filters['reversed'] = reversed
# This should always be the last statement!
import Blog.views
