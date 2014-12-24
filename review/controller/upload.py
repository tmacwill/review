import simplejson
from flask import render_template, request, session, redirect, url_for

import review.controller.common
import review.model.upload
import review.model.user
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
                    "contents": f.stream.read()
                })

        id = review.model.upload.create(user_id, request.form.get('name', "Unnamed"), files)
        return simplejson.dumps({"success": True, "id": id})

@app.route('/view/<slug>')
def view(slug):
    upload = review.model.upload.upload_for_slug(slug)
    if upload is None:
        return render_template("error.html", error="Invalid Url")

    files = review.model.upload.files_for_upload(upload["id"])
    return render_template("view.html", name=upload["name"], files=simplejson.dumps(files))

@app.route('/uploads', methods=['GET'])
def uploads():
    user_id = review.controller.common.require_user()
    uploads_info = review.model.upload.get_all_by_user_id(user_id)

    return render_template("uploads.html", uploads=uploads_info)

