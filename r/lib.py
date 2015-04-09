from flask import render_template
import random
import simplejson
import string
import time

_slug_alphabet = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)

def fail_response(data=None):
    if not data:
        data = {}

    data['success'] = False
    return to_json(data)

def from_json(json: str):
    return simplejson.loads(json)

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

    return render_template(template_name, **kwargs)

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
