import pymysql
import time
from flask import g

DATABASE = 'review'
USER = 'root'

def connect_db():
    """Connects to the specific database."""
    conn = pymysql.connect(database=DATABASE, user=USER, autocommit=True)
    return conn

"""
Following functions copied from Flask examples. will be replaced with a MySQL engine
"""
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pymysql'):
        g.pymysql = connect_db()
    return g.pymysql

#@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'pymysql'):
        g.pymysql.close()

def query(sql, args=()):
    """Queries the database and returns cursor"""
    cur = get_db().cursor(pymysql.cursors.DictCursor)
    cur.execute(sql, args)
    return cur

def get(sql, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = query(sql, args)
    res = cur.fetchall()
    return (res[0] if res else None) if one else res

"""
Returns the current time in ms since the epoch
"""
def get_current_time():
    return int(time.time() * 1000)
