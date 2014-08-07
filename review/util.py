import uuid

def generate_slug(length=32):
    """ Returns a slug, up to 32 characters long """
    if length < 0:
        length = 0
    if length > 32:
        length = 32
    return uuid.uuid4().hex[0:length-1]
