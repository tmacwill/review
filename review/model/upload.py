import review.cache
import review.db
import review.model.file
import review.util

def create(user_id: int, name: str, files: list) -> int:
    """ Upload a set of files from a user. """

    sql = """
        INSERT INTO uploads
            (user_id, name, slug, creation_time)
        VALUES
            (%s, %s, %s, %s)
    """
    slug = review.util.generate_slug()
    result = review.db.query(sql, (user_id, name, slug, review.util.now()))
    upload_id = result.lastrowid

    review.model.file.create(upload_id, files)
    return slug

def get_all_by_user_id(user_id: int, num=None, offset=None):
    """ Get uploads for a given user. """
    return review.db.get_where('uploads', {'user_id': user_id})

def upload_for_slug(slug: str) -> int:
    """ Returns the upload id for a given slug """
    res = review.db.get_where('uploads', {'slug': slug}, one=True)
    if len(res) == 0:
        return None
    else:
        return res
