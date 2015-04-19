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

    @classmethod
    def after_set(cls, rows, result):
        # dirty counts when new notifications are created
        dirtied = set()
        for row in rows:
            user_id = row.get('user_id')
            if user_id and not user_id in dirtied:
                get_unread_count_for_user.dirty(user_id)

        return rows

class types(object):
    new_review = 1

def create_if_new_review(user_id: str, from_user_id: str, upload_id: str):
    """ Create a new review notification. """

    # don't create a notification to yourself
    if user_id == from_user_id:
        return

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
    users = r.model.user.User.get([user_id, from_user_id], metadata={'filter': False})
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

    r.email.send(
        subject='New Review!',
        recipients=[users[user_id].email],
        plaintext="%s reviewed your upload %s! Visit http://letsreview.io/review/%s to read your review." % (users[from_user_id].name, upload.name, upload.slug),
        html="%s reviewed your upload %s! <a href='http://letsreview.io/review/%s' target='_blank'>Click here</a> to read your review." % (users[from_user_id].name, upload.name, upload.slug)
    )

@r.store.cached()
def get_unread_count_for_user(user_id: str):
    return Notification.get_count_where({
        'user_id': user_id,
        'is_read': 0
    })

def get_for_feed(user_id: str):
    """ Get notifications, along with relevant associations. """

    # get the 100 most recent notifications
    notifications = Notification.get_where({
        'user_id': r.model.user.current_user(),
    }, limit=100, order='creation_time DESC')

    # get the users who sent those notifications
    users = r.model.user.User.get([e.from_user_id for e in notifications.values()])

    # decode metadata and attach user object
    for notification in notifications.values():
        notification.metadata = r.lib.from_json(notification.metadata)
        notification.from_user = users[notification.from_user_id]

    return notifications
