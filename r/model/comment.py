import itertools
import r.db

class Comment(r.db.DBObject):
    __table__ = 'comments'

def get_by_file_ids(file_ids: list) -> dict:
    return r.model.comment.Comment.get_where({'file_id': file_ids})
