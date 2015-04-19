from flask import request
import r
from r import app

@app.route('/comment', methods=['POST'])
@r.renderer.login_required
def create():
    comment = r.model.comment.Comment.set({
        'id': request.form.get('id'),
        'user_id': r.model.user.current_user(),
        'file_id': request.form.get('file_id'),
        'line': int(request.form.get('line', 0)),
        'contents': request.form.get('contents')
    })

    return r.renderer.success({'id': comment[0]['id']})

@app.route('/comment/<comment_id>', methods=['DELETE'])
@r.renderer.login_required
def delete(comment_id):
    comment = r.model.comment.Comment.get(comment_id)
    if not comment or comment.user_id != r.model.user.current_user():
        return r.renderer.fail()

    r.model.comment.Comment.delete(comment_id)
    return r.renderer.success()
