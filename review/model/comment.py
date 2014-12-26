import review.db
import review.util

def create(user_id: int, file_id: int, line: int, contents: str) -> int:
    """ Create a new comment. """

    sql = """
        INSERT INTO comments
            (user_id, file_id, line, contents)
        VALUES
            (%s, %s, %s, %s)
    """

    res = review.db.query(sql, (user_id, file_id, line, contents))
    return res.lastrowid

def get_for_files(file_ids: list) -> list:
    """ Get all the comments for a file. """

    sql = """
        SELECT * FROM comments
        WHERE file_id IN %s
    """ % review.db.values(file_ids)

    return review.db.get(sql)

def delete(comment_id: int):
    """ Delete a comment. """

    sql = """
        DELETE FROM comments
        WHERE id = %s
    """

    review.db.query(sql, (comment_id,))

def update(comment_id: int, contents: str):
    """ Update the contents of a comment. """

    sql = """
        UPDATE comments
        SET contents = %s
        WHERE id = %s
    """

    review.db.query(sql, (contents, comment_id))
