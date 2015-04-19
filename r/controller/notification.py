import arrow
from flask import request
import r
from r import app

@app.route('/notifications', methods=['GET'])
def notifications():
    existing = r.model.notification.get_for_feed(r.model.user.current_user())

    # convert timestamp to a relative format
    for notification in existing.values():
        notification.creation_time = arrow.get(r.lib.from_timestamp(notification.creation_time)).humanize()

    return r.renderer.page('pages/notifications.html', notifications=existing)

@app.before_request
def mark_notification_in_url():
    notification_id = request.args.get('__nid__')
    if not notification_id:
        return

    # mark notification as read
    notification = r.model.notification.Notification.get(notification_id)
    r.model.notification.Notification.set({
        'id': notification_id,
        'user_id': notification.user_id,
        'is_read': 1
    })
