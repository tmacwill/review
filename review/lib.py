import simplejson
import time
import uuid

def generate_slug():
    """ Returns a 32-character slug. """

    return uuid.uuid4().hex

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
