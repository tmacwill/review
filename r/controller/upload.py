import urllib.parse
from flask import request, redirect
from collections import OrderedDict

import r
from r import app

@app.route('/', methods=['GET'])
@app.route('/browse', methods=['GET'])
def browse():
    tags = {}
    popular_tags = r.model.tag.popular_tags()
    query_tags = request.args.get('q')
    if query_tags:
        tags = r.model.tag.Tag.get(query_tags.split(','))

    return r.lib.render(
        'pages/browse.html',
        popular_tags=popular_tags,
        tags=tags,
        tags_json=r.lib.to_json(tags)
    )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    user_id = r.model.user.current_user()
    if request.method == 'GET':
        return r.lib.render('pages/upload.html')

    else:
        files = []
        for file in request.form.getlist('files[]'):
            data = r.lib.from_json(urllib.parse.unquote(file))
            files.append({
                'filename': data['filename'],
                'contents': data['contents']
            })

        upload = r.model.upload.create_with_files(user_id, request.form['name'], request.form['description'],
            files, request.form.getlist('tags[]'))
        return redirect('/review/' + upload['slug'])

@app.route('/review/<slug>')
def view(slug):
    upload = r.model.upload.get_by_slug(slug)
    if upload is None:
        return r.lib.render('error.html', error='Invalid URL')

    # get everything associated with this upload
    current_user = r.model.user.current_user()
    files = r.model.file.get_highlighted_for_upload(upload.id)
    comments = r.model.comment.Comment.get_where({'file_id': list(files.keys())}, order='creation_time ASC')
    users = r.model.user.User.get([comment.user_id for comment in comments.values()] + [upload.user_id, current_user])
    tags = r.model.tag.get_by_upload_id(upload.id)

    grouped_comments = OrderedDict()
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
    )
