import memcache
import inspect
import functools
import base64
import operator
from flask import g

SERVERS = [
    '127.0.0.1:11211'
]

def _client():
    """ Get a reference to the thread-local client instance. """

    if not hasattr(g, '_cache'):
        g._cache = memcache.Client(SERVERS, debug=0)
    return g._cache

def _path_for_function(f):
    """ Get the module path to a function. """

    return f.__module__ + '.' + f.__name__

def _cache_key(f, *args, **kwargs):
    """ Serialize a function call into a unique string.

    Get the full path to the current module, then base64-encode all parameters
    in lexicographical order, separated by colons.
    """

    key = _path_for_function(f)
    sorted_args = sorted(inspect.getcallargs(f, *args, **kwargs).items(), key=operator.itemgetter(0))
    for k, v in sorted_args:
        key += ':' + base64.b64encode(bytes(str(v), 'utf-8')).decode('utf-8')

    return key

def cached(timeout=0):
    """ Caching decorator. """

    def decorator(f):
        def wrapper(*args, **kwargs):
            # check if value already exists in cache
            key = _cache_key(f, *args, **kwargs)
            cached = _client().get(key)
            if cached is not None:
                return cached

            # value is not cached, so compute and store
            result = f(*args, **kwargs)
            _client().set(key, result, time=timeout)

            # also keep track of all the keys associated with this function,
            # so we can later clear them all in a single pass
            all_keys_key = _path_for_function(f)
            all_keys = _client().get(all_keys_key)
            if not all_keys or not isinstance(all_keys, set):
                all_keys = set()

            # add this key to the list of all keys and store
            all_keys.add(key)
            _client().set(all_keys_key, all_keys)

            return result

        # create functions for dirtying cache values
        wrapper.dirty = functools.partial(dirty, f)
        wrapper.dirty_all = functools.partial(dirty_all, f)
        return wrapper
    return decorator

def dirty(f, *args, **kwargs):
    """ Dirty the cache key for the function invoked with the given parameters. """

    _client().delete(_cache_key(f, *args, **kwargs))

def dirty_all(f):
    """ Dirty all cache keys for the function (i.e., any parameters). """

    key = _path_for_function(f)
    keys = _client().get(key) or set()
    _client().delete_multi(set([key]) | keys)
