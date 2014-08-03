from review import app
from review.db import query_db

def get(options={}, one=False):
    args = []
    if len(options) > 0:
        where_str = "WHERE "

        # include n-1 ANDs (e.g. a=? AND b=? AND c=?)
        where_str += "=? AND ".join(options.keys()) + "=?"

        # create args array
        args = list(options.values())
    else:
        where_str = ""

    res = query_db("SELECT * FROM users %s" % where_str, args, one=one)
    return res
