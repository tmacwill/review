import builtins
import memcache
import inspect
import functools
import base64
import operator
from flask import g

SERVERS = [
    '127.0.0.1:11211'
]

ALL_KEYS_PREFIX = 'a:'
INCLUDED_KEYS_PREFIX = 'i:'

def _client():
    """ Get a reference to the thread-local client instance. """

    if not hasattr(g, '_cache'):
        g._cache = memcache.Client(SERVERS, debug=0)
    return g._cache

def _path_for_function(f):
    """ Get the module path to a function. """

    return f.__module__ + '.' + f.__name__

def _sorted_parameters(f, *args, **kwargs):
    """ Get the parameters passed to a function as sorted key-value pairs. """

    return sorted(inspect.getcallargs(f, *args, **kwargs).items(), key=operator.itemgetter(0))

def _cache_key(f, sorted_parameters=None, prefix=''):
    """ Serialize a function call into a unique string.

    Get the full path to the current module, then base64-encode all parameters
    in lexicographical order, separated by colons.
    """

    sorted_parameters = sorted_parameters or []
    key = prefix + _path_for_function(f)
    for k, v in sorted_parameters:
        key += ':' + base64.b64encode(bytes(str(v), 'utf-8')).decode('utf-8')

    return key

def cached(timeout=0, exclude=None):
    """ Caching decorator. """

    def decorator(f):
        def wrapper(*args, **kwargs):
            # check if value already exists in cache
            sorted_parameters = _sorted_parameters(f, *args, **kwargs)
            key = _cache_key(f, sorted_parameters)
            cached = get(key)
            if cached is not None:
                return cached

            # value is not cached, so compute and store
            result = f(*args, **kwargs)
            set(key, result, timeout=timeout)

            # if this function has specified a list of keys to exclude, then we need to store a separate
            # list mapping a key without those parameters to a list of keys with those parameters
            included_keys_key = None
            if exclude:
                # keep track of the excluded parameters so we have it when we dirty later
                excluded_set = builtins.set(exclude)
                if not hasattr(f, '__exclude'):
                    f.__exclude = excluded_set

                # get a list of parameters without the keys designated excluded
                included_parameters = [e for e in sorted_parameters if e[0] not in excluded_set]
                included_keys_key = _cache_key(f, included_parameters, INCLUDED_KEYS_PREFIX)
                included_keys = get(included_keys_key)

                # add the current key to that set of keys
                if not included_keys or not isinstance(included_keys, builtins.set):
                    included_keys = builtins.set()
                included_keys.add(key)
                set(included_keys_key, included_keys)

            # also keep track of all the keys associated with this function,
            # so we can later clear them all in a single pass
            all_keys_key = _cache_key(f, prefix=ALL_KEYS_PREFIX)
            all_keys = get(all_keys_key)
            if not all_keys or not isinstance(all_keys, builtins.set):
                all_keys = builtins.set()

            # add this key to the list of all keys and store
            all_keys.add(key)
            if included_keys_key:
                all_keys.add(included_keys_key)
            set(all_keys_key, all_keys)

            return result

        # create functions for dirtying cache values
        wrapper.dirty = functools.partial(dirty, f)
        return wrapper
    return decorator

def delete(key):
    """ Delete a value from the cache. """

    return _client().delete(key)

def delete_multi(keys, key_prefix=''):
    """ Delete multiple values from the cache. """

    return _client().delete_multi(keys, key_prefix=key_prefix)

def dirty(f, *args, **kwargs):
    """ Dirty the cache key for the function invoked with the given parameters. """

    # delete the key containing the cached value for this function
    sorted_parameters = _sorted_parameters(f, *args, **kwargs)
    keys_to_delete = builtins.set([_cache_key(f, sorted_parameters)])

    # if we're called with no arguments, then dirty everything
    dirty_all = len(args) == 0 and len(kwargs) == 0
    if dirty_all:
        all_keys_key = _cache_key(f, prefix=ALL_KEYS_PREFIX)
        keys = get(all_keys_key) or builtins.set()
        keys_to_delete |= keys
        keys_to_delete.add(all_keys_key)

    # if we have keys to be excluded, then dirty all of those as well
    if hasattr(f, '__exclude'):
        included_parameters = [e for e in sorted_parameters if e[0] not in f.__exclude]
        included_keys_key = _cache_key(f, included_parameters, INCLUDED_KEYS_PREFIX)
        keys = get(included_keys_key) or builtins.set()
        keys_to_delete |= keys

    return delete_multi(keys_to_delete)

def get(key: str, debug=False):
    """ Get a value from the cache. """

    return _client().get(key)

def get_multi(keys: list, key_prefix=''):
    """ Get multiple values from the cache. """

    return _client().get_multi(keys, key_prefix=key_prefix)

def set(key: str, value, timeout=0):
    """ Set a new value in the cache. """

    _client().set(key, value, time=timeout)
    return value

def set_multi(mapping: dict, timeout=0, key_prefix=''):
    """ Get multiple values from the cache. """

    return _client().set_multi(mapping, time=timeout, key_prefix=key_prefix)
