from flask import session, redirect, url_for
import review.model.user
from werkzeug.routing import RequestRedirect


def require_user(return_page="login"):
    """ Returns user_id of logged in user, or redirects if no user is logged in """
    user_id = review.model.user.current_user()
    if user_id is None:
        raise RequestRedirect(url_for(return_page))

    return user_id

