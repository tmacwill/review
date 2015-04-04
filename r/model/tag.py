import r

class Tag(r.db.DBObject):
    __table__ = 'tags'

def get_by_upload_id(upload_id: str) -> dict:
    tag_uploads = r.model.tag_upload.TagUpload.get_where({'upload_id': upload_id})
    return Tag.get([e.tag_id for e in tag_uploads.values()])

def popular_tags(limit=10) -> list:
    """ The most popular tags. """

    # cheating for now, implement ranking at some point
    result = [{
        'id': '0r3duxIXjBR5',
        'name': 'Python'
    }, {
        'id': '5LRhUWrm9E47',
        'name': 'Javascript'
    }, {
        'id': '68dqGMsHc71B',
        'name': 'C'
    }]

    return [Tag(tag) for tag in result[:limit]]

def with_prefix(prefix: str, limit=10) -> list:
    """ Get all the tags with the given prefix. """

    if not prefix:
        return popular_tags(limit)

    # this is pretty slow and simple for now. we should instead implement this with
    # an in-memory store or redis
    sql = """
        SELECT * FROM tags
        WHERE name LIKE %s
        LIMIT %s
    """

    result = r.db.get(sql, (prefix + '%', limit))
    return [Tag(tag) for tag in result]
