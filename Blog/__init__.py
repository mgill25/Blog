from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config.from_envvar('BLOG_SETTINGS')

# minify and bundle the css
assets = Environment(app)
css = Bundle('css/style.css', filters='cssmin', output='css/style.min.css')
assets.register('css_main', css)

# Register a jijna filter.
app.jinja_env.filters['reversed'] = reversed
# This should always be the last statement!
import Blog.views
