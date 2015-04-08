import itertools
import r

class Comment(r.db.DBObject):
    __table__ = 'comments'
    __foreign_key__ = 'comment_id'
    __belongs_to__ = lambda: {
        "user": {
            "model": r.model.user.User,
            "foreign_key": "user_id"
        },
        "file": {
            "model": r.model.file.File,
            "foreign_key": "file_id"
        }
    }
