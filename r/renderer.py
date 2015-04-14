from flask import render_template
from flask import make_response
import datetime
import r

def _add_current_user(data):
    if not 'current_user_json' in data:
        uid = r.model.user.current_user()
        if not uid:
            data['current_user'] = False
            data['current_user_json'] = 'false'
        else:
            user = r.model.user.User.get(uid)
            data['current_user'] = user
            data['current_user_json'] = r.lib.to_json(user)

    return data

def fail(data=None):
    """ API failure response. """

    if not data:
        data = {}

    data['success'] = False
    return r.lib.to_json(data)

def page(template_name, **kwargs):
    """ Render a template. """

    _add_current_user(kwargs)

    # disable caching
    response = make_response(render_template(template_name, **kwargs))
    response.headers['Last-Modified'] = datetime.datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def success(data=None):
    """ API success response. """

    if not data:
        data = {}

    data['success'] = True
    return r.lib.to_json(data)
