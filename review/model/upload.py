import review.cache, review.db, review.util
import pygments, pygments.lexers, pygments.formatters
import uuid

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

    sql = """
        INSERT INTO upload_files
            (upload_id, filename, contents)
        VALUES
            %s
        """ % ','.join([review.db.values([upload_id, e['filename'], e['contents']]) for e in files])
    review.db.query(sql)

    return slug

def highlight(text: str, filename: str) -> str:
    """ Syntax highlights text (from provided filename). Returns HTML as a string """
    lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    formatter = pygments.formatters.HtmlFormatter(linenos="table", linespans="line", anchorlinenos=True, lineanchors=filename)
    return '<style>' + formatter.get_style_defs() + '</style>' + pygments.highlight(text, lexer, formatter)

def get_all_by_user_id(user_id: int, num=None, offset=None):
    """ Get uploads for a given user. """
    return review.db.get_where('uploads', {"user_id": user_id})

def upload_for_slug(slug: str) -> int:
    """ Returns the upload id for a given slug """
    res = review.db.get_where('uploads', {"slug": slug}, one=True)
    if len(res) == 0:
        return None
    else:
        return res["id"]

@review.cache.cached()
def files_for_upload(upload_id: int) -> list:
    """ Get file info for an upload. """
    res = review.db.get_where('upload_files', {"upload_id": upload_id})

    # highlight before sending
    for f in res:
        f["contents"] = highlight(f["contents"], f["filename"])

    return res
