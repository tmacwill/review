from flask import render_template
from flask import make_response
import datetime
import random
import simplejson
import string
import time
from r import app

_slug_alphabet = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)

def fail_response(data=None):
    if not data:
        data = {}

    data['success'] = False
    return to_json(data)

def from_json(json: str):
    return simplejson.loads(json)

def from_timestamp(timestamp: int):
    return datetime.datetime.fromtimestamp(timestamp / 1000)

def generate_slug(length=12):
    """ Returns a unique slug of the specified length. """

    return ''.join(random.sample(_slug_alphabet, length))

def now():
    """ Get the current time. """

    return int(time.time() * 1000)

def render(template_name, **kwargs):
    """ Render a template. """

    import r.model.user
    if not 'current_user_json' in kwargs:
        uid = r.model.user.current_user()
        if not uid:
            kwargs['current_user'] = False
            kwargs['current_user_json'] = 'false'
        else:
            user = r.model.user.User.get(uid)
            kwargs['current_user'] = user
            kwargs['current_user_json'] = to_json(user)

    # disable caching
    response = make_response(render_template(template_name, **kwargs))
    response.headers['Last-Modified'] = datetime.datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def success_response(data=None):
    if not data:
        data = {}

    data['success'] = True
    return to_json(data)

def to_json(obj):
    """ Serialize an object to JSON. """

    def encode(obj):
        if hasattr(obj, '__to_json__'):
            return obj.__to_json__()
        return obj

    return simplejson.dumps(obj, default=encode)
