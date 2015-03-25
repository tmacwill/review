from flask import request
import r
from r import app

@app.route('/comment', methods=['POST'])
def create():
    data = {
        'user_id': r.model.user.current_user(),
        'file_id': request.form.get('file_id'),
        'line': int(request.form.get('line', 0)),
        'contents': request.form.get('contents')
    }

    if request.form.get('id'):
        data['id'] = request.form.get('id')

    comment = r.model.comment.Comment.set(data)
    return r.lib.success_response({'id': comment[0]['id']})

@app.route('/comment/<comment_id>', methods=['DELETE'])
def delete(comment_id):
    comment = r.model.comment.Comment.get(comment_id, one=True)
    if not comment or comment.user_id != r.model.user.current_user():
        return r.lib.fail_response()

    r.model.comment.Comment.delete(comment_id)
    return r.lib.success_response()
