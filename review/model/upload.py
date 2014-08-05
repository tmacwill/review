import review.db

def create(user_id, files):
    """ Upload a set of files from a user. """

    sql = """
        INSERT INTO uploads
            (user_id, creation_time)
        VALUES
            (%s, %s)
    """
    result = review.db.query(sql, (user_id, review.db.now()))
    upload_id = result.lastrowid

    sql = """
        INSERT INTO upload_files
            (upload_id, filename, contents, creation_time)
        VALUES
            %s
    """ % ','.join([review.db.values([upload_id, e['filename'], e['contents'], review.db.now()]) for e in files])
    review.db.query(sql)

    return upload_id
