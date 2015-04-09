import r

class Comment(r.db.DBObject):
    __table__ = 'comments'
    __foreign_key__ = 'comment_id'
    __belongs_to__ = lambda: {
        'user': {
            'model': r.model.user.User,
            'foreign_key': 'user_id'
        },
        'file': {
            'model': r.model.file.File,
            'foreign_key': 'file_id'
        }
    }

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            # a comment might be the first on an upload, in which case we need a notification
            if not row.get('id') and row.get('user_id') and row.get('file_id'):
                file = r.model.file.File.get(row['file_id'])
                upload = r.model.upload.Upload.get(file.upload_id)
                r.model.notification.create_if_new_review(
                    user_id=upload.user_id,
                    from_user_id=row['user_id'],
                    upload_id=file.upload_id
                )

        return rows

def has_commented(user_id: str, upload_id: str) -> bool:
    """ Whether or not a user has commented on an upload. """

    files = r.model.file.File.get_where({'upload_id': upload_id})
    return Comment.get_count_where({'user_id': user_id, 'file_id': [e.id for e in files.values()]}) > 0
