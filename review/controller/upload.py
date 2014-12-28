import simplejson
from flask import render_template, request, session, redirect, url_for

import review.controller.common
import review.model.comment
import review.model.file
import review.model.upload
from review import app, db

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        user_id = review.controller.common.require_user()
        files = []
        for key in request.files:
            for f in request.files.getlist(key):
                files.append({
                    "filename": f.filename,
                    "contents": f.stream.read().decode()
                })

        id = review.model.upload.create(user_id, request.form.get('name', "Unnamed"), files)
        return simplejson.dumps({"success": True, "id": id})

@app.route('/view/<slug>')
def view(slug):
    upload = review.model.upload.upload_for_slug(slug)
    if upload is None:
        return render_template("error.html", error="Invalid Url")

    # get the files for this upload and the comments associated with those files
    files = review.model.file.get_for_upload(upload['id'])
    comments = review.model.comment.get_for_files([e['id'] for e in files])

    return render_template("view.html", name=upload['name'], files=simplejson.dumps(files), comments=simplejson.dumps(comments))

@app.route('/uploads', methods=['GET'])
def uploads():
    user_id = review.controller.common.require_user()
    uploads_info = review.model.upload.get_all_by_user_id(user_id)

    return render_template("uploads.html", uploads=uploads_info)

