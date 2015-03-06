import flask.ext.assets
from r import app

assets = flask.ext.assets.Environment(app)

assets.register('js/lib', flask.ext.assets.Bundle(
    'js/lib/jquery-1.11.1.min.js',
    'js/lib/underscore-min.js',
    'js/lib/nunjucks.min.js',
    output='build/js/lib.min.js'
))
