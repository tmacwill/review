import itertools
import review.db

class Comment(review.db.DBObject):
    __table__ = 'comments'

def get_by_files(file_ids: list) -> dict:
    comments = review.model.comment.Comment.get_where({'file_id': file_ids})
    return dict((k, list(v)) for k, v in itertools.groupby(comments, lambda e: e.file_id))
