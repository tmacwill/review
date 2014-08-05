from review import app
import review.db
from werkzeug.security import generate_password_hash, check_password_hash

def _generate_api_key():
    return "TODO"

def get(options={}, one=False):
    args = []
    if len(options) > 0:
        where_str = "WHERE "

        # include n-1 ANDs (e.g. a=? AND b=? AND c=?)
        where_str += "=%s AND ".join(options.keys()) + "=%s"

        # create args array
        args = list(options.values())
    else:
        where_str = ""

    res = review.db.get("SELECT * FROM users %s" % where_str, args, one=one)
    return res

def add(name, email, password):
    """ Insert user into DB. Returns ID of new user, or None on error"""
    hash = generate_password_hash(password)
    current_time = review.db.get_current_time()
    api_key = _generate_api_key()

    # TODO - decide how to handle errors
    res = review.db.query("INSERT INTO users (name, email, password, api, creation_time) VALUES (%s, %s, %s, %s, %s)", [name, email, hash, api_key, current_time])

    return res.lastrowid
