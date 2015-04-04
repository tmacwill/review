import pygments, pygments.lexers, pygments.formatters
import r

class TableHTMLFormatter(pygments.formatters.HtmlFormatter):
    def wrap(self, source, outfile):
        # wrap the entire output in a single table
        yield 0, '<table class="file-contents-table">'
        yield 0, '<tbody>'
        yield 0, '<tr class="first-row"><td class="line-number padding">&nbsp;</td><td class="code padding">&nbsp;</td></tr>'

        # each line of source code is a row in the table, with the line numbers in one cell and the code in another
        line_number = 1
        for i, t in source:
            line = '<tr>'
            line += '<td class="line-number"><a href="#" data-line="%s">%s</a></td>' % (line_number, line_number)
            line += '<td class="code" data-line="%s">%s</td>' % (line_number, t)
            line += '</tr>'
            yield i, line

            line_number += 1

        yield 0, '</tbody>'
        yield 0, '</table>'

class File(r.db.DBObject):
    __table__ = 'files'
    __foreign_key__ = 'file_id'

    __belongs_to__ = lambda: {
        "upload": {
            "model": r.model.upload.Uploads,
            "foreign_key": "upload_id"
        }
    }
    __has_many__ = lambda: {
        "comments": {
            "model": r.model.comment.Comment,
            "foreign_key": "user_id"
        }
    }

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            if not row.get('id'):
                row['line_count'] = len(row['contents'].split("\n"))

        return rows

def get_highlighted_for_upload(upload_id: str) -> list:
    """ Get highlighted versions of the files for an upload. """

    rows = File.get_where({'upload_id': upload_id})
    for row in rows.values():
        row.contents = highlight(row.contents, row.filename)

    return rows

def highlight(text: str, filename: str) -> str:
    """ Syntax highlights text (from provided filename). Returns HTML as a string. """

    lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    formatter = TableHTMLFormatter()
    return '<style>' + formatter.get_style_defs() + '</style>' + pygments.highlight(text, lexer, formatter)
