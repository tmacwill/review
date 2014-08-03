import pymysql
from flask import g

DATABASE = 'review'
USER = 'root'

def connect_db():
    """Connects to the specific database."""
    conn = pymysql.connect(database=DATABASE, user=USER)
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

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    res = cur.fetchall()
    return (res[0] if res else None) if one else res
