from review import app, db
from flask import render_template, request, session, redirect, url_for
import review.model.upload

@app.route('/upload', methods=['POST'])
def submission():
    json = request.get_json()
    review.model.upload.create(1, json.get('files', []))
    return 'done\n'
