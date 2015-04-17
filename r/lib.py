import datetime
import random
import simplejson
import string
import time
from r import app

_slug_alphabet = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)

def from_json(json: str):
    return simplejson.loads(json)

def from_timestamp(timestamp: int):
    return datetime.datetime.fromtimestamp(timestamp / 1000)

def generate_slug(length=12):
    """ Returns a unique slug of the specified length. """

    return ''.join(random.sample(_slug_alphabet, length))

def now():
    """ Get the current time. """

    return int(time.time() * 1000)

def to_json(obj):
    """ Serialize an object to JSON. """

    def encode(obj):
        if hasattr(obj, '__to_json__'):
            return obj.__to_json__()
        return obj

    return simplejson.dumps(obj, default=encode)
