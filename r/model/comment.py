import itertools
import r.db

class Comment(r.db.DBObject):
    __table__ = 'comments'

def get_by_files(file_ids: list) -> dict:
    comments = r.model.comment.Comment.get_where({'file_id': file_ids})
    return itertools.groupby(comments, lambda e: e.file_id)
