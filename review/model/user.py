import review.db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

def _generate_api_key():
    return "TODO"

def add(name, email, password):
    """ Insert user into DB. Returns ID of new user, or None on error"""

    # TODO - decide how to handle errors
    sql = """
        INSERT INTO users
            (name, email, password, api, creation_time)
        VALUES
            (%s, %s, %s, %s, %s)
    """
    res = review.db.query(sql, [name, email, generate_password_hash(password), _generate_api_key(), review.db.now()])
    return res.lastrowid

def get_by_email(email):
    return review.db.get_where('users', {"email": email}, one=True)

def current_user():
    return session.get("user_id", None)
