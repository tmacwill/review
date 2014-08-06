import flask.ext.assets
from review import app

assets = flask.ext.assets.Environment(app)

assets.register('js/lib', flask.ext.assets.Bundle(
    'js/lib/jquery-1.11.1.min.js',
    'js/lib/bootstrap.min.js',
    output='build/js/lib.min.js'
))

assets.register('css/lib', flask.ext.assets.Bundle(
    'css/lib/bootstrap.min.css',
    output='build/css/lib.min.css'
))
