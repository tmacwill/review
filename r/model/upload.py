import r

class Upload(r.db.DBObject):
    __table__ = 'uploads'
    __foreign_key__ = 'upload_id'

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            if not row.get('id'):
                row['slug'] = r.lib.generate_slug()

        return rows

def create_with_files(user_id: str, name: str, description: str, files: list, tags: list) -> str:
    """ Create a new upload with a set of files. """

    # create a new upload
    upload = Upload.set({
        'description': description,
        'name': name,
        'user_id': user_id
    })[0]

    # associate files with upload
    r.model.file.File.set([{
        'upload_id': upload['id'],
        'filename': file['filename'],
        'contents': file['contents']
    } for file in files])

    # associate tags with upload
    r.model.tag_upload.TagUpload.set([{
        'upload_id': upload['id'],
        'tag_id': tag
    } for tag in tags])

    return upload

def get_by_slug(slug: str):
    """ Get the upload matching the given slug. """
    return Upload.get_where({'slug': slug}, one=True)

def get_with_tags(tag_ids: list, limit=300) -> list:
    """ Get uploads with the given tags. """

    tag_uploads = r.model.tag_upload.TagUpload.get_where({'tag_id': tag_ids}, limit=300, order='creation_time DESC')
    return Upload.get_where({'id': [e.upload_id for e in tag_uploads.values()]}, limit=50, order='creation_time DESC')
