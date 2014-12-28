import simplejson
from flask import render_template, request, session, redirect, url_for

import review.controller.common
import review.model.comment
from review import app, db

@app.route('/comment', methods=['POST'])
def create():
    user_id = review.controller.common.require_user()
    comment_id = int(request.form.get('comment_id', 0))
    file_id = int(request.form.get('file_id', 0))
    line = int(request.form.get('line', 0))
    contents = request.form.get('contents', '')

    # if we're given an ID, then update an existing comment
    if comment_id:
        review.model.comment.update(comment_id, contents)

    # if we're not given an ID, then create a new comment
    else:
        comment_id = review.model.comment.create(user_id, file_id, line, contents)

    return review.controller.common.success_response({'comment_id': comment_id})
