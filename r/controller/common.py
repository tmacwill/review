from flask import session, redirect, url_for
from werkzeug.routing import RequestRedirect
import simplejson
import r.model.user
from r import app

def require_user(return_page="login"):
    """ Returns user_id of logged in user, or redirects if no user is logged in """

    user_id = r.model.user.current_user()
    if user_id is None:
        return None

    return user_id
