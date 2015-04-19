import builtins
import memcache
import inspect
import functools
import base64
import operator
import pickle
import redis
from flask import g

_DEFAULT_SHARD = '_d'
_instances = {}

INCLUDED_KEYS_PREFIX = '_i:'

def _client(shard_id):
    """ Get a reference to the thread-local client instance. """

    return _instances[shard_id]

def _flush_I_KNOW_WHAT_IM_DOING(shard=_DEFAULT_SHARD):
    """ Flush everything. You better know what you're doing. """

    _client(shard).flushall()

def _path_for_function(f):
    """ Get the module path to a function. """

    return f.__module__ + '.' + f.__name__

def _sorted_parameters(f, *args, **kwargs):
    """ Get the parameters passed to a function as sorted key-value pairs. """

    return sorted(inspect.getcallargs(f, *args, **kwargs).items(), key=operator.itemgetter(0))

def _cache_key(f, sorted_parameters=None, prefix='', version=0):
    """ Serialize a function call into a unique string.

    Get the full path to the current module, then base64-encode all parameters
    in lexicographical order, separated by colons.
    """

    sorted_parameters = sorted_parameters or []
    key = ''
    if prefix:
        key += prefix + ':'

    key += str(version) + ':' + _path_for_function(f)
    for k, v in sorted_parameters:
        key += ':' + base64.b64encode(bytes(str(v), 'utf-8')).decode('utf-8')

    return key

def cached(timeout=3600, version=0, shard=_DEFAULT_SHARD, wildcard=None):
    """ Caching decorator. """

    def decorator(f):
        def wrapper(*args, **kwargs):
            if not hasattr(f, '__version'):
                f.__version = version

            if not hasattr(f, '__shard'):
                f.__shard = shard

            # check if value already exists in cache
            sorted_parameters = _sorted_parameters(f, *args, **kwargs)
            key = _cache_key(f, sorted_parameters, version=version)
            cached = get(key, shard)
            if cached is not None:
                return cached

            # value is not cached, so compute and store
            result = f(*args, **kwargs)
            set(key, result, shard, timeout=timeout)

            # if this function has specified a list of keys to wildcard, then we need to store a separate
            # list mapping a key without those parameters to a list of keys with those parameters
            included_keys_key = None
            if wildcard:
                # keep track of the excluded parameters so we have it when we dirty later
                wildcard_set = builtins.set(wildcard)
                if not hasattr(f, '__wildcard'):
                    f.__wildcard = wildcard_set

                # get a list of parameters without the keys designated excluded
                included_parameters = [e for e in sorted_parameters if e[0] not in wildcard_set]
                included_keys_key = _cache_key(f, included_parameters, INCLUDED_KEYS_PREFIX, version=version)
                included_keys = get(included_keys_key, shard)

                # add the current key to that set of keys
                if not included_keys or not isinstance(included_keys, builtins.set):
                    included_keys = builtins.set()
                included_keys.add(key)
                set(included_keys_key, included_keys, shard)

            return result

        # create functions for dirtying cache values
        wrapper.dirty = functools.partial(dirty, f)
        return wrapper
    return decorator

def configure(shards: dict=None):
    if not shards:
        shards = {
            _DEFAULT_SHARD: {
                'host': 'localhost',
                'port': 6379
            }
        }

    for shard_id, data in shards.items():
        _instances[shard_id] = redis.StrictRedis(host=data['host'], port=data['port'])

def delete(key: str, shard=_DEFAULT_SHARD, key_prefix=''):
    """ Delete a value from the cache. """

    _client(shard).delete(key_prefix + key)

def delete_multi(keys: list, shard=_DEFAULT_SHARD, key_prefix=''):
    """ Delete multiple values from the cache. """

    pipe = pipeline(shard)
    for key in keys:
        pipe.delete(key_prefix + key)
    pipe.execute()

def dirty(f, *args, **kwargs):
    """ Dirty the cache key for the function invoked with the given parameters. """

    # delete the key containing the cached value for this function
    version = f.__version
    shard = f.__shard
    sorted_parameters = _sorted_parameters(f, *args, **kwargs)
    keys_to_delete = builtins.set([_cache_key(f, sorted_parameters, version=version)])

    # if we have keys to be excluded, then dirty all of those as well
    if hasattr(f, '__wildcard'):
        included_parameters = [e for e in sorted_parameters if e[0] not in f.__wildcard]
        included_keys_key = _cache_key(f, included_parameters, INCLUDED_KEYS_PREFIX, version=version)
        keys = get(included_keys_key, shard) or builtins.set()
        keys_to_delete |= keys

    return delete_multi(keys_to_delete, shard)

def execute(command, args=None, shard=_DEFAULT_SHARD):
    """ Execute a command directly on the store backend. """

    if not args:
        args = tuple()

    if not isinstance(args, tuple):
        args = (args,)

    return getattr(_client(shard), command)(*args)

def get(key, shard=_DEFAULT_SHARD, key_prefix=''):
    """ Get a single value from the cache. """

    result = _client(shard).get(key_prefix + key)
    if not result:
        return result

    return pickle.loads(result)

def get_multi(keys: list, shard=_DEFAULT_SHARD, key_prefix=''):
    """ Get a value from the cache. """

    pipe = pipeline(shard)
    for key in keys:
        if key and isinstance(key, str):
            pipe.get(key_prefix + key)

    result_list = pipe.execute()
    result = {}
    for key, value in zip(keys, result_list):
        if value is not None:
            result[key] = pickle.loads(value)

    return result

def pipeline(shard=_DEFAULT_SHARD):
    """ Get a pipeline that can be used to batch commands. """

    return _client(shard).pipeline()

def set(key: str, value, shard=_DEFAULT_SHARD, key_prefix='', timeout=0):
    """ Set a new value in the cache. """

    pipe = pipeline(shard)
    pipe.set(key_prefix + key, pickle.dumps(value))
    if timeout:
        pipe.expire(key_prefix + key, timeout)

    pipe.execute()

def set_multi(mapping: dict, shard=_DEFAULT_SHARD, key_prefix='', timeout=0):
    """ Set multiple values in the cache. """

    pipe = pipeline(shard)
    for key, value in mapping.items():
        pipe.set(key_prefix + key, pickle.dumps(value))
        if timeout:
            pipe.expire(key_prefix + key, timeout)

    pipe.execute()
