from review import app, db
import review.controller.common
from flask import render_template, request, session, redirect, url_for
import review.model.upload
import review.model.user

@app.route('/upload', methods=['POST'])
def upload():
    user_id = review.controller.common.require_user()
    json = request.get_json()
    review.model.upload.create(user_id, json.get('name', "Unnamed"), json.get('files', []))
    return 'done\n'

@app.route('/view/<slug>')
def view(slug):
    upload_id = review.model.upload.upload_for_slug(slug)
    if upload_id is None:
        return render_template("error.html", error="Invalid Url")

    files = review.model.upload.files_for_upload(upload_id)
    return render_template("files.html", files=files)

@app.route('/uploads', methods=['GET'])
def uploads():
    user_id = review.controller.common.require_user()
    uploads_info = review.model.upload.get_all_by_user_id(user_id)

    return render_template("uploads.html", uploads=uploads_info)

