import simplejson
from flask import render_template, request, session, redirect, url_for

import r.controller.common
import r.model.comment
import r.model.file
import r.model.upload
import r.model.user
import r.model.tag
import r.lib
from r import app, db

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    user_id = r.model.user.current_user()
    if request.method == 'GET':
        return render_template('pages/upload.html')

    else:
        files = []
        for key in request.files:
            for f in request.files.getlist(key):
                if f.filename:
                    files.append({
                        'filename': f.filename,
                        'contents': f.stream.read().decode()
                    })

        upload = r.model.upload.create_with_files(user_id, request.form['name'], request.form['description'],
            files, request.form.getlist('tags[]'))
        return redirect('/review/' + upload['slug'])

@app.route('/review/<slug>')
def view(slug):
    upload = r.model.upload.get_by_slug(slug)
    if upload is None:
        return render_template('error.html', error='Invalid URL')

    # get everything associated with this upload
    current_user = r.model.user.current_user()
    files = r.model.file.get_highlighted_for_upload(upload.id)
    comments = r.model.comment.get_by_file_ids(list(files.keys()))
    users = r.model.user.User.get([comment.user_id for comment in comments.values()] + [upload.user_id, current_user])
    tags = r.model.tag.get_by_upload_id(upload.id)

    grouped_comments = {}
    for comment in comments.values():
        grouped_comments.setdefault(comment.file_id, [])
        grouped_comments[comment.file_id].append(comment)

    return r.lib.render(
        'pages/review.html',
        upload=upload,
        files=files.values(),
        grouped_comments=grouped_comments,
        tags=tags,
        users=users,
        user_json=r.lib.to_json(users[current_user])
    )
