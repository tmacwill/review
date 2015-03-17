import r.cache
import r.db
import pygments, pygments.lexers, pygments.formatters

class File(r.db.DBObject):
    __table__ = 'files'

def get_highlighted_for_upload(upload_id: str) -> list:
    """ Get highlighted versions of the files for an upload. """

    rows = File.get_where({'upload_id': upload_id})
    for row in rows.values():
        row.contents = highlight(row.contents, row.filename)

    return rows

def highlight(text: str, filename: str) -> str:
    """ Syntax highlights text (from provided filename). Returns HTML as a string. """

    lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    formatter = pygments.formatters.HtmlFormatter(linenos="table", linespans="line", anchorlinenos=True, lineanchors=filename)
    return '<style>' + formatter.get_style_defs() + '</style>' + pygments.highlight(text, lexer, formatter)
