import review.db, review.util
import uuid

def create(user_id, name, files):
    """ Upload a set of files from a user. """

    sql = """
        INSERT INTO uploads
            (user_id, name, slug, creation_time)
        VALUES
            (%s, %s, %s, %s)
    """
    slug = review.util.generate_slug()
    result = review.db.query(sql, (user_id, name, slug, review.db.now()))
    upload_id = result.lastrowid

    sql = """
        INSERT INTO upload_files
            (upload_id, filename, contents, creation_time)
        VALUES
            %s
    """ % ','.join([review.db.values([upload_id, e['filename'], e['contents'], review.db.now()]) for e in files])
    review.db.query(sql)

    return upload_id

def get_all_by_user_id(user_id, num=None, offset=None):
    """ Get uploads for a given user. """
    return review.db.get_where('uploads', {"user_id": user_id})

def upload_for_slug(slug):
    """ Returns the upload id for a given slug """
    res = review.db.get_where('uploads', {"slug": slug}, one=True)
    if len(res) == 0:
        return None
    else:
        return res["id"]

def files_for_upload(upload_id):
    """ Get file info for an upload. """
    return review.db.get_where('upload_files', {"upload_id": upload_id})

