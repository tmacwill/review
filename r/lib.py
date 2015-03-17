from flask import render_template
import simplejson
import time
import uuid

def generate_slug():
    """ Returns a 32-character slug. """

    return uuid.uuid4().hex

def now():
    """ Get the current time. """

    return int(time.time() * 1000)

def render(template_name, **kwargs):
    """ Render a template. """

    import r.model.user
    if not 'current_user_json' in kwargs:
        uid = r.model.user.current_user()
        if not uid:
            kwargs['current_user_json'] = 'false'
        else:
            user = r.model.user.User.get(uid)
            kwargs['current_user_json'] = to_json(user[uid])

    return render_template(template_name, **kwargs)

def success_response(data=None):
    if not data:
        data = {}

    data['success'] = True
    return simplejson.dumps(data)

def to_json(obj):
    """ Serialize an object to JSON. """

    def encode(obj):
        if hasattr(obj, '__to_json__'):
            return obj.__to_json__()
        return obj

    return simplejson.dumps(obj, default=encode)
