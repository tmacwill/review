import review.cache, review.db, review.util
import pygments, pygments.lexers, pygments.formatters

def create(upload_id: int, files: list):
    """ Store a list of files associatd with an upload. """

    # if files isn't given as a list, then make it one
    if not isinstance(files, list):
        files = [files]

    sql = """
        INSERT INTO files
            (upload_id, filename, contents)
        VALUES
            %s
        """ % ','.join([review.db.values([upload_id, e['filename'], e['contents']]) for e in files])

    review.db.query(sql)

def get_for_upload(upload_id: int) -> list:
    """ Get file info for an upload. """

    result = review.db.get_where('files', {'upload_id': upload_id})

    # highlight before sending
    for f in result:
        f['contents'] = highlight(f['contents'], f['filename'])

    return result

def highlight(text: str, filename: str) -> str:
    """ Syntax highlights text (from provided filename). Returns HTML as a string """

    lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    formatter = pygments.formatters.HtmlFormatter(linenos="table", linespans="line", anchorlinenos=True, lineanchors=filename)
    return '<style>' + formatter.get_style_defs() + '</style>' + pygments.highlight(text, lexer, formatter)
