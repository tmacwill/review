import operator
import pymysql
import time
from flask import g
from r import app
import r.cache
import r.lib

DATABASE = 'review'
USER = 'root'

def _generate_id():
    return r.lib.generate_slug()

def _connect_db():
    """ Connects to the specific database. """
    conn = pymysql.connect(database=DATABASE, user=USER, autocommit=True)
    return conn

def _cache_key(table, id=''):
    return 'gbi:' + table + ':' + id

def _get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pymysql'):
        g.pymysql = _connect_db()
    return g.pymysql

def columns(c):
    """ Format SQL columns. """
    if isinstance(c, str):
        return '`' + c + '`'

    return '(' + ','.join(['`' + e + '`' for e in c]) + ')'

@app.teardown_appcontext
def close_db(error):
    """ Closes the database again at the end of the request. """
    if hasattr(g, 'pymysql'):
        g.pymysql.close()

def escape(sql):
    """ Escape a SQL string. """
    return _get_db().escape(str(sql))

def get(sql, args=(), one=False):
    """ Queries the database and returns a list of dictionaries. """

    cur = query(sql, args)
    res = cur.fetchall()

    # split so that falsy values become empty list
    if not res:
        return None if one else []

    return res[0] if one else res

def get_where(table, options=None, limit=None, offset=None, order=None, one=False, columns='*', dry=False):
    options = options or {}
    args = []
    where = ''
    if len(options) > 0:
        where += 'WHERE '
        for k, v in options.items():
            # for lists, construct a WHERE IN clase
            if isinstance(v, list):
                where += k + " IN %s AND " % values(v)

            # for scalars, use escaped values
            else:
                where += k + '=%s AND '
                args.append(v)

        # stupid hack to remove the last "AND ". I'm a bad programmer.
        where = where[:-4]

    query = "SELECT %s FROM %s %s" % (columns, table, where)
    if limit:
        query += " LIMIT %s" % limit
    if offset:
        query += " OFFSET %s" % offset
    if order:
        query += " ORDER BY %s" % order

    # in dry run mode, return the query instead of executing it right away
    if dry:
        return query

    result = get(query, args, one)
    return result

def query(sql, args=None, skip_cache=False):
    """ Queries the database and returns cursor. """

    cur = _get_db().cursor(pymysql.cursors.DictCursor)
    if args is not None:
        cur.execute(sql, args)
    else:
        cur.execute(sql)

    return cur

def values(v):
    """ Convert a list of values into a SQL list of values. """
    return '(' + ', '.join(escape(e) for e in v) + ')'

class DBObject(object):
    __table__ = None
    __timeout__ = 3600

    def __init__(self, fields):
        self.__fields__ = list(fields.keys())
        for k, v in fields.items():
            setattr(self, k, v)

    def __repr__(self):
        result = super(DBObject, self).__repr__()
        result += ' (' + ', '.join([i + '=' + str(getattr(self, i)) for i in self.__fields__ if hasattr(self, i)]) + ')'
        return result

    def __to_json__(self):
        result = {k: getattr(self, k) for k in self.__fields__}
        return result

    @classmethod
    def _cache_key(cls, id=''):
        """ The cache key for an object in the table. """
        return 'db:' + cls.__table__ + ':' + id

    @classmethod
    def after_delete(cls, ids):
        return

    @classmethod
    def after_get(cls, rows):
        return rows

    @classmethod
    def after_set(cls, rows, result):
        return result.lastrowid

    @classmethod
    def before_delete(cls, ids):
        return

    @classmethod
    def before_get(cls, ids):
        return ids

    @classmethod
    def before_set(cls, rows):
        return rows

    @classmethod
    def delete(cls, ids):
        cls.before_delete(ids)

        # delete by the primary key
        sql = "DELETE FROM %s WHERE id IN" % (cls.__table__, values(ids))
        result = query(sql)

        # dirty the cache for deleted rows
        cls.dirty(ids)
        cls.after_delete(ids)

        return result

    @classmethod
    def dirty(cls, ids):
        """ Dirty multiple objects by their ids. """

        if not isinstance(ids, list):
            ids = [ids]

        r.cache.delete_multi(ids, key_prefix=cls._cache_key())

    @classmethod
    def get(cls, ids, one=False):
        """ Get rows by ID, fetching and storing uncached values appropriately. """

        ids = cls.before_get(ids)

        # try to grab all of the objects at once
        key_prefix = cls._cache_key(cls.__table__)
        values = r.cache.get_multi(ids, key_prefix=key_prefix)

        # if every value was found, then we're done
        if len(ids) == len(values):
            return values

        # determine which ids haven't been fetched yet
        ids = set(ids)
        cached_ids = set(values.keys())
        uncached_ids = [id for id in ids if id not in cached_ids]

        # grab the remaining ids from the database, then cache them in a single multi-set
        remaining = get_where(cls.__table__, {'id': uncached_ids})
        cache_mapping = {}
        for value in remaining:
            cache_mapping[value['id']] = cls(value)
        r.cache.set_multi(cache_mapping, key_prefix=key_prefix, timeout=cls.__timeout__)

        # return the union of the cached and uncached values
        values.update(cache_mapping)

        # if we don't want a dictionary, then take the first value
        if one:
            values = values.popitem()[1]

        return cls.after_get(values)

    @classmethod
    def get_count_where(cls, options=None):
        result = get_where(cls.__table__, options, one=True, columns='COUNT(id) AS c')
        return result['c']

    @classmethod
    def get_ids(cls, options=None, limit=None, offset=None, order=None, one=False, dry=False):
        rows = get_where(
            cls.__table__,
            options=options,
            limit=limit,
            offset=offset,
            order=order,
            one=one,
            columns='id',
            dry=dry
        )

        return [row['id'] for row in rows]

    @classmethod
    def get_where(cls, options=None, limit=None, offset=None, order=None, one=False):
        ids = cls.get_ids(options, limit=limit, offset=offset, order=order)
        return cls.get(ids, one=one)

    @classmethod
    def set(cls, rows):
        if not isinstance(rows, list):
            rows = [rows]

        rows = cls.before_set(rows)

        # for new rows, generate IDs and creation times
        for row in rows:
            if not row.get('id'):
                row['id'] = _generate_id()
                row['creation_time'] = r.lib.now()

        # each row may specify different columns, so group by unique fields
        grouped = {}
        for row in rows:
            k = tuple(sorted(row.keys()))
            grouped.setdefault(k, [])
            grouped[k].append(row)

        # we need a separate query for each distinct group of columns
        result = None
        for fields, row_values in grouped.items():
            sql = "INSERT INTO %s " % (cls.__table__)
            sql += columns(fields)
            sql += ' VALUES '
            values_to_create = []
            for row_value in row_values:
                values_to_create.append(values([str(e[1]) for e in sorted(row_value.items(), key=operator.itemgetter(0))]))
            sql += ','.join(values_to_create)

            # so we can use this for both inserts and updates, add a duplicate key clause
            sql += ' ON DUPLICATE KEY UPDATE '
            sql += ','.join([columns(field) + '=VALUES(' + columns(field) + ')' for field in fields])
            result = query(sql)

        # dirty the cache for affected rows
        cls.dirty([row['id'] for row in rows])

        return cls.after_set(rows, result)
