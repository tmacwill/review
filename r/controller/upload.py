import simplejson
from flask import render_template, request, session, redirect, url_for

import r.controller.common
import r.model.comment
import r.model.file
import r.model.upload
import r.lib
from r import app, db

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    else:
        user_id = r.controller.common.require_user()
        files = []
        for key in request.files:
            for f in request.files.getlist(key):
                files.append({
                    'filename': f.filename,
                    'contents': f.stream.read().decode()
                })

        id = r.model.upload.create(user_id, request.form.get('name', 'Unnamed'), files)
        return simplejson.dumps({'success': True, 'id': id})

@app.route('/review/<slug>')
def view(slug):
    upload = r.model.upload.get_by_slug(slug)
    if upload is None:
        return render_template('error.html', error='Invalid URL')

    files = r.model.file.File.get_highlighted_for_upload(upload.id)
    return render_template('review.html', upload=upload, files=files.values())
