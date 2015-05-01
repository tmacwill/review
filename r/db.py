import builtins
import operator
import pymysql
import time
from flask import g
from collections import OrderedDict
import r
from r import app

DATABASE = 'review'
USER = 'root'

def _generate_id():
    return r.lib.generate_slug()

def _connect_db():
    """ Connects to the specific database. """
    conn = pymysql.connect(database=DATABASE, user=USER, autocommit=True)
    return conn

def _filter_fields(fields):
    """ Filter out invalid field names. """

    exclude = builtins.set(['__created__'])
    return [e for e in fields if e not in exclude]

def _filter_values(row):
    """ Filter out invalid values. """

    return {k: v for k, v in row.items() if k in _filter_fields(row.keys())}

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
    if order:
        query += " ORDER BY %s" % order
    if limit:
        query += " LIMIT %s" % limit
    if offset:
        query += " OFFSET %s" % offset

    # in dry run mode, return the query instead of executing it right away
    if dry:
        return query

    result = get(query, args, one)
    return result

def query(sql, args=None):
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
    __version__ = 0

    __has_many__ = lambda: {}
    __belongs_to__ = lambda: {}

    def __init__(self, fields):
        self.__initial_fields__ = _filter_fields(fields.keys())
        self.__fields__ = _filter_fields(fields.keys())
        for k, v in fields.items():
            setattr(self, k, v)

    def __setattr__(self, name, value):
        if hasattr(self, '__fields__'):
            self.__fields__.append(name)

        object.__setattr__(self, name, value)

    def __repr__(self):
        result = super(DBObject, self).__repr__()
        result += ' (' + ', '.join([i + '=' + str(getattr(self, i)) for i in self.__initial_fields__ if hasattr(self, i)]) + ')'
        return result

    def __to_json__(self):
        result = {k: getattr(self, k) for k in self.__fields__ if hasattr(self, k)}
        return result

    @classmethod
    def _cache_key(cls, id=''):
        """ The cache key for an object in the table. """

        return "db:%s:%s:%s" % (cls.__table__, cls.__version__, id)

    @classmethod
    def after_delete(cls, ids):
        return

    @classmethod
    def after_get(cls, rows, metadata=None):
        return rows

    @classmethod
    def after_set(cls, rows, result):
        return rows

    @classmethod
    def before_delete(cls, ids):
        return

    @classmethod
    def before_get(cls, ids, metadata=None):
        return ids

    @classmethod
    def before_set(cls, rows):
        return rows

    @classmethod
    def delete(cls, ids):
        if not isinstance(ids, list):
            ids = [ids]

        cls.before_delete(ids)

        # delete by the primary key
        sql = "DELETE FROM %s WHERE id IN %s" % (cls.__table__, values(ids))
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

        r.store.delete_multi([cls._cache_key(id) for id in ids])

    @classmethod
    def get(cls, ids, metadata=None):
        return cls.get_by_id(ids, one=isinstance(ids, str), metadata=metadata)

    @classmethod
    def get_by_id(cls, ids, one=False, metadata=None):
        """ Get rows by ID, fetching and storing uncached values appropriately. """

        if not isinstance(ids, list):
            ids = [ids]

        if len(ids) == 0:
            return None if one else {}

        ids = cls.before_get(ids, metadata=metadata)

        # try to grab all of the objects at once
        ids = list(set(ids))
        key_prefix = cls._cache_key()
        values = r.store.get_multi(ids, key_prefix=key_prefix)

        # if every value was found, then we're done
        if len(ids) == len(values):
            if one:
                values = values.popitem()[1]
            return cls.after_get(values, metadata=metadata)

        # determine which ids haven't been fetched yet
        ids = set(ids)
        cached_ids = set(values.keys())
        uncached_ids = [id for id in ids if id not in cached_ids]

        # grab the remaining ids from the database, then cache them in a single multi-set
        remaining = get_where(cls.__table__, {'id': uncached_ids})
        cache_mapping = {}
        for value in remaining:
            cache_mapping[value['id']] = cls(value)
        r.store.set_multi(cache_mapping, key_prefix=key_prefix, timeout=cls.__timeout__)

        # return the union of the cached and uncached values
        values.update(cache_mapping)

        # if we don't want a dictionary, then take the first value
        if one:
            values = values.popitem()[1]

        return cls.after_get(values, metadata=metadata)

    @classmethod
    def get_count_where(cls, options=None):
        result = get_where(cls.__table__, options, one=True, columns='COUNT(id) AS c')
        return result['c']

    @classmethod
    def get_ids_where(cls, options=None, limit=None, offset=None, order=None, one=False, dry=False):
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
    def get_where(cls, options=None, limit=None, offset=None, order=None, one=False, metadata=None, associations=None):
        ids = cls.get_ids_where(options, limit=limit, offset=offset, order=order)
        if not ids:
            return None if one else {}

        cls_data = cls.get_by_id(ids, one=one, metadata=metadata)

        if associations is None:
            associations = {}
        if isinstance(associations, list):
            associations = _build_associations_dict(associations)

        for k,v in associations.items():
            # look up association in __has_many__ and __belongs_to__
            for assoc_type in [cls.__has_many__, cls.__belongs_to__]:
                d = assoc_type()

            for cls_id, cls_item in cls_data.items():
                setattr(cls_item, k, {})

            has_many = cls.__has_many__()
            if k in has_many:
                association = has_many[k]["model"]
                foreign_key = has_many[k]["foreign_key"]

                association_data = association.get_where({foreign_key: ids}, associations=v)
                for assoc_id, assoc_item in association_data.items():
                    foreign_key_id = getattr(assoc_item, foreign_key)
                    getattr(cls_data[foreign_key_id], k)[assoc_id] = assoc_item

            belongs_to = cls.__belongs_to__()
            if k in belongs_to:
                association = belongs_to[k]["model"]
                foreign_key = belongs_to[k]["foreign_key"]

                foreign_ids = [getattr(cls_item, foreign_key) for cls_item in cls_data.values()]
                association_data = association.get_where({'id': foreign_ids}, associations=v)

                for cls_item in cls_data.values():
                    setattr(cls_item, k, association_data[getattr(cls_item, foreign_key)])

        if not order:
            return cls_data

        # if we have an order by clause, then IDs will be in sorted order, so return
        # an OrderedDict in order to preserve that ordering
        result = OrderedDict()
        for id in ids:
            result[id] = cls_data[id]

        return result

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
                row['__created__'] = True

        # each row may specify different columns, so group by unique fields
        grouped = {}
        for row in rows:
            k = tuple(sorted(_filter_fields(row.keys())))
            grouped.setdefault(k, [])
            grouped[k].append(_filter_values(row))

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

def _build_associations_dict(associations_list):
    """
    Converts, e.g. ["users", "users.comments"] to
    {
        "users": {"comments": {}}
    }
    """
    final_result = {}
    for assoc_str in associations_list:
        pieces = assoc_str.split('.')
        result = final_result
        for piece in pieces:
            result.setdefault(piece, {})
            result = result[piece]
    return final_result
