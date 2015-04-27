from flask import redirect
from flask import request
from flask import render_template
from flask import make_response
import datetime
import functools
import urllib.parse
import r

def _add_badge_counts(data):
    user_id = r.model.user.current_user()
    if not user_id:
        return

    data['notifications_badge'] = r.model.notification.get_unread_count_for_user(user_id)

def _add_current_user(data):
    if not 'current_user_json' in data:
        user_id = r.model.user.current_user()
        if not user_id:
            data['current_user'] = False
            data['current_user_json'] = 'false'
        else:
            user = r.model.user.User.get(user_id)
            data['current_user'] = user
            data['current_user_json'] = r.lib.to_json(user)

    return data

def error(status_code=404, **kwargs):
    """ Return an error page according to the status code. """

    return page('pages/errors/%s.html' % status_code, status_code=status_code, **kwargs)

def fail(data=None):
    """ API failure response. """

    if not data:
        data = {}

    data['success'] = False
    return r.lib.to_json(data)

def login_required(f):
    """ Decorator to enforce the user is logged in. """

    @functools.wraps(f)
    def inner(*args, **kwargs):
        redirect_url = '/login'
        user_id = r.model.user.current_user()
        if not user_id:
            # return a failure json response if this is an ajax request
            if request.is_xhr:
                return fail({'login_required': True})

            # redirect to login page for a regular request
            query = urllib.parse.parse_qs(redirect_url)
            query['next'] = urllib.parse.quote(request.path + "?%s" % request.query_string.decode('utf-8'))
            return redirect(redirect_url + "?%s" % urllib.parse.urlencode(query))

        return f(*args, **kwargs)
    return inner

def page(template_name, status_code=None, **kwargs):
    """ Render a template. """

    _add_current_user(kwargs)
    _add_badge_counts(kwargs)
    response = make_response(render_template(template_name, **kwargs))

    # disable caching
    response.headers['Last-Modified'] = datetime.datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'

    if status_code:
        response.status_code = status_code

    return response

def success(**kwargs):
    """ API success response. """

    data = kwargs
    if not data:
        data = {}

    data['success'] = True
    return r.lib.to_json(data)
