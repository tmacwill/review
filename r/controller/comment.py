import simplejson
from flask import render_template, request, session, redirect, url_for

import r.controller.common
import r.model.comment
from r import app, db

@app.route('/comment', methods=['POST'])
def create():
    user_id = r.controller.common.require_user()
    comment_id = int(request.form.get('comment_id', 0))
    file_id = int(request.form.get('file_id', 0))
    line = int(request.form.get('line', 0))
    contents = request.form.get('contents', '')

    # if we're given an ID, then update an existing comment
    if comment_id:
        r.model.comment.update(comment_id, contents)

    # if we're not given an ID, then create a new comment
    else:
        comment_id = r.model.comment.create(user_id, file_id, line, contents)

    return r.controller.common.success_response({'comment_id': comment_id})
