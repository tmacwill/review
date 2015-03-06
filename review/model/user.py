import review.cache
import review.db
import review.lib
import copy
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

class User(review.db.DBObject):
    __table__ = 'users'

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            # hash password
            if row.get('password'):
                row['password'] = generate_password_hash(row['password'])

            # if row represents a new user, then generate an API key
            if not row.get('id'):
                row['creation_time'] = review.lib.now()

        return rows

    @classmethod
    def after_get(cls, rows):
        # remove fields like password for gets by default
        if isinstance(rows, list):
            return [_filter(row) for row in rows]
        return _filter(rows)


def _filter(user, password=True, api=True):
    u = copy.copy(user)
    if password and hasattr(u, 'password'):
        del u.password
    if api and hasattr(u, 'api'):
        del u.api

    return u

def _generate_api_key() -> str:
    return review.lib.generate_slug()

def current_user() -> int:
    return int(session.get('user_id', None))

def get_by_email(email: str, filter=True) -> dict:
    user = User.get_where({'email': email}, one=True)
    if filter:
        user = _filter(user)

    return user

# @review.cache.cached()
def get_by_username(username: str, filter=True) -> dict:
    user = User.get_where({'username': username}, one=True)
    if filter:
        user = _filter(user)

    return user
