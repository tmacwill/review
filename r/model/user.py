import copy
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import r

class User(r.db.DBObject):
    __table__ = 'users'
    __foreign_key__ = 'user_id'
    __has_many__ = lambda: {
        "comments": {
            "model": r.model.comment.Comment,
            "foreign_key": "user_id"
        },
        "uploads": {
            "model": r.model.upload.Upload,
            "foreign_key": "user_id"
        }
    }

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            # hash password
            if row.get('password'):
                row['password'] = generate_password_hash(row['password'])

            # if row represents a new user, then generate an API key
            if not row.get('id'):
                row['creation_time'] = r.lib.now()

        return rows

    @classmethod
    def after_get(cls, rows, metadata=None):
        metadata = metadata or {}
        if not metadata.get('filter', True):
            return rows

        # remove fields like password for gets by default
        if isinstance(rows, list):
            return [_filter(row) for row in rows]
        elif isinstance(rows, dict):
            result = {}
            for k, v in rows.items():
                result[k] = _filter(v)
            return result

        return _filter(rows)


def _filter(user, password=True, api=True, email=True):
    u = copy.copy(user)
    if password and hasattr(u, 'password'):
        del u.password
    if api and hasattr(u, 'api'):
        del u.api
    if email and hasattr(u, 'email'):
        del u.email

    return u

def _generate_api_key() -> str:
    return r.lib.generate_slug()

def current_user() -> int:
    return session.get('user_id')

def get_by_email(email: str, filter=True) -> dict:
    user = User.get_where({'email': email}, one=True, metadata={'filter': filter})
    if filter:
        user = _filter(user)

    return user

def get_by_username(username: str, filter=True) -> dict:
    user = User.get_where({'username': username}, one=True, metadata={'filter': filter})
    if filter:
        user = _filter(user)

    return user
