import r

class Upload(r.db.DBObject):
    __table__ = 'uploads'
    __foreign_key__ = 'upload_id'

    __has_many__ = lambda: {
        "files": {
            "model": r.model.file.File,
            "foreign_key": "upload_id"
        },
        "tag_uploads": {
            "model": r.model.tag_upload.TagUpload,
            "foreign_key": "upload_id"
        }
    }

    __belongs_to__ = lambda: {
        "user": {
            "model": r.model.user.User,
            "foreign_key": "user_id"
        }
    }

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

def get_by_slug(slug: str) -> Upload:
    """ Get the upload matching the given slug. """

    return Upload.get_where({'slug': slug}, one=True)

def get_with_tags(tag_ids: list, limit=300) -> list:
    """ Get uploads with the given tags. """

    tag_uploads = r.model.tag_upload.TagUpload.get_where({'tag_id': tag_ids}, limit=300, order='creation_time DESC')
    return Upload.get_where({'id': [e.upload_id for e in tag_uploads.values()]}, limit=50, order='creation_time DESC')

def _prepare_upload_for_story(upload):
    """
    Modifies an upload in place to include necessary fields for the story box
    """
    comment_count = sum(len(file.comments) for file in upload.files.values())
    upload._comment_count = comment_count

    line_count = sum(file.line_count for file in upload.files.values())
    upload._line_count = line_count
    return upload

def uploads_for_feed(user_id: str):
    uploads = r.model.upload.Upload.get_where({'user_id': user_id}, associations=['files', 'files.comments', 'tag_uploads.tag', 'user'], order='creation_time DESC')
    # compute comment and line counts for each upload
    for upload in uploads.values():
        _prepare_upload_for_story(upload)

    return uploads

def reviews_for_feed(user_id: str):
    # determine which uploads have a comment by this user
    comments = r.model.comment.Comment.get_where({'user_id': user_id}, associations=['file'])

    review_upload_ids = set()
    for comment in comments.values():
        review_upload_ids.add(comment.file.upload_id)

    uploads = r.model.upload.Upload.get_where(
        {'id': list(review_upload_ids)},
        associations=['files', 'files.comments', 'tag_uploads.tag', 'user'],
        order='creation_time DESC'
    )

    # compute comment and line counts for each upload
    for upload in uploads.values():
        _prepare_upload_for_story(upload)

    return uploads
