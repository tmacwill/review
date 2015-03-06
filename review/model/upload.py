import review.cache
import review.db
import review.model.file
import review.lib

class Upload(review.db.DBObject):
    __table__ = 'uploads'

    @classmethod
    def before_set(cls, rows):
        for row in rows:
            if not row.get('id'):
                row['slug'] = review.lib.generate_slug()

        return rows

def get_by_slug(slug: str):
    return Upload.get_where({'slug': slug}, one=True)
