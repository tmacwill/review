import r.cache
import r.db
import r.model.file
import r.model.tag_upload
import r.lib

class Upload(r.db.DBObject):
    __table__ = 'uploads'

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            if not row.get('id'):
                row['slug'] = r.lib.generate_slug()

        return rows

def get_by_slug(slug: str):
    return Upload.get_where({'slug': slug}, one=True)

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
