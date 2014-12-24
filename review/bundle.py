import flask.ext.assets
from review import app

assets = flask.ext.assets.Environment(app)

assets.register('js/lib', flask.ext.assets.Bundle(
    'js/lib/jquery-1.11.1.min.js',
    'js/lib/underscore-min.js',
    'components/lib/platform/platform.js',
    output='build/js/lib.min.js'
))
