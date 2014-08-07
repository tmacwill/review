import pymysql
import time
from flask import g
from review import app

DATABASE = 'review'
USER = 'root'

def _connect_db():
    """Connects to the specific database."""
    conn = pymysql.connect(database=DATABASE, user=USER, autocommit=True)
    return conn

def _get_db():
    """ Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pymysql'):
        g.pymysql = _connect_db()
    return g.pymysql

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'pymysql'):
        g.pymysql.close()

def query(sql, args=()):
    """Queries the database and returns cursor"""
    cur = _get_db().cursor(pymysql.cursors.DictCursor)
    cur.execute(sql, args)
    return cur

def get(sql, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = query(sql, args)
    res = cur.fetchall()
    # split so that falsy values become empty list
    if not res:
        return []
    return res[0] if one else res

def get_where(table, options={}, one=False):
    args = []
    if len(options) > 0:
        where_str = "WHERE "

        # include n-1 ANDs (e.g. a=? AND b=? AND c=?)
        where_str += "=%s AND ".join(options.keys()) + "=%s"

        # create args array
        args = list(options.values())
    else:
        where_str = ""

    cur = query("SELECT * FROM %s %s" % (table, where_str), args)
    res = cur.fetchall()

    # split so that falsy values become empty list
    if not res:
        return []
    return res[0] if one else res

def now():
    """ Get the current time. """
    return int(time.time() * 1000)

def escape(sql):
    """ Escape a SQL string. """
    return _get_db().escape(str(sql))

def values(v):
    """ Convert a list of values into a SQL list of values. """
    return '(' + ', '.join(escape(e) for e in v) + ')'
