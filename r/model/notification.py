import r

class Notification(r.db.DBObject):
    __table__ = 'notifications'
    __foreign_key__ = 'notification_id'
    __belongs_to__ = lambda: {
        'user': {
            'model': r.model.user.User,
            'foreign_key': 'user_id'
        },
    }

class types(object):
    new_review = 1

def create_if_new_review(user_id: str, from_user_id: str, upload_id: str):
    """ Create a new review notification. """

    # get existing notifications between these two users
    existing = Notification.get_where({
        'user_id': user_id,
        'from_user_id': from_user_id,
        'notification_type': types.new_review
    }, limit=1000, order='creation_time DESC')

    # if a notification already exists for this upload, then don't create another one
    for notification in existing.values():
        metadata = r.lib.from_json(notification.metadata)
        if metadata['upload_id'] == upload_id:
            return

    # create the notification
    upload = r.model.upload.Upload.get(upload_id)
    Notification.set({
        'user_id': user_id,
        'from_user_id': from_user_id,
        'notification_type': types.new_review,
        'metadata': r.lib.to_json({
            'upload_id': upload.id,
            'upload_name': upload.name,
            'upload_slug': upload.slug,
        })
    })

def get_for_feed(user_id: str):
    """ Get notifications, along with relevant associations. """

    # get the 100 most recent notifications
    notifications = r.model.notification.Notification.get_where({
        'user_id': r.model.user.current_user(),
    }, limit=100, order='creation_time DESC')

    # get the users who sent those notifications
    users = r.model.user.User.get([e.from_user_id for e in notifications.values()])

    for notification in notifications.values():
        notification.metadata = r.lib.from_json(notification.metadata)
        notification.from_user = users[notification.from_user_id]

    return notifications
