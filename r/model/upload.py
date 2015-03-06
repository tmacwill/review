import r.cache
import r.db
import r.model.file
import r.lib

class Upload(r.db.DBObject):
    __table__ = 'uploads'

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            if not row.get('id'):
                row['slug'] = r.lib.generate_slug()

        return rows

def get_by_slug(slug: str):
    return Upload.get_where({'slug': slug}, one=True)
