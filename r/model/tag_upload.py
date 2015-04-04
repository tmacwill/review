import r

class TagUpload(r.db.DBObject):
    __table__ = 'tags_uploads'
    __belongs_to__ = lambda: {
        "tag": {
            "model": r.model.tag.Tag,
            "foreign_key": "tag_id"
        },
        "upload": {
            "model": r.model.upload.Upload,
            "foreign_key": "upload_id"
        }
    }
