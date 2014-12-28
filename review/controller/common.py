from flask import session, redirect, url_for
from werkzeug.routing import RequestRedirect
import simplejson
import review.model.user
from review import app


def require_user(return_page="login"):
    """ Returns user_id of logged in user, or redirects if no user is logged in """

    user_id = review.model.user.current_user()
    if user_id is None:
        raise RequestRedirect(url_for(return_page))

    return user_id

def success_response(data=None):
    if not data:
        data = {}

    data['success'] = True
    return simplejson.dumps(data)
