import r

_autocomplete_key = 'tags_autocomplete'

class Tag(r.db.DBObject):
    __table__ = 'tags'
    __foreign_key__ = 'tag_id'

    __has_many__ = lambda: {
        "tag_uploads": {
            "model": r.model.tag_upload.TagUpload,
            "foreign_key": "upload_id"
        }
    }

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

def sync_to_store():
    """ Sync all tags to the store, for autocomplete purposes. """

    # clear previous tags
    r.store.delete(_autocomplete_key)

    # get the total number of tags
    n = Tag.get_count_where()
    batch_size = 1000

    # iterate over batches of tags so we don't overload the store
    for i in range(n // batch_size + 1):
        tags = Tag.get_where(limit=batch_size, offset=i * batch_size, order='creation_time ASC')
        pipeline = r.store.pipeline()
        for tag in tags.values():
            data = {'name': tag.name, 'id': tag.id}
            pipeline.zadd(_autocomplete_key, 0, "%s:%s" % (tag.name.lower(), r.lib.to_json(data)))

        pipeline.execute()

def with_prefix(prefix: str, limit=10) -> list:
    """ Get all the tags with the given prefix. """

    if not prefix:
        return popular_tags(limit)

    # query store for tags
    prefix = prefix.lower()
    tags = r.store.execute('zrangebylex', (_autocomplete_key, "[%s" % prefix, "[%s\xff" % prefix))

    # extract data from each tag
    ids = []
    for tag in tags[:limit]:
        data = tag.decode('utf-8').split(':', 1)

        if len(data) < 2:
            continue

        # tags have a colon for a delimiter between name and metadata
        json = r.lib.from_json(data[1])
        ids.append(json['id'])

    return list(Tag.get(ids).values())
