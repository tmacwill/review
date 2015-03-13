from r import app, db
from flask import render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import r.model.user
import r.cache

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Register user. """

    # create new user on POST
    if request.method == 'POST':
        # if email or passwords not provided, fail
        if request.form['name'] == '' or request.form['email'] == '' or request.form['password'] == '' or request.form['password2'] == '':
            return render_template("error.html", error="Please enter an email address and password.")

        # make sure passwords match
        if request.form['password'] != request.form['password2']:
            return render_template("error.html", error="Passwords must match.")

        # else, look for email in db
        user = r.model.user.get_by_email(request.form['email'], filter=False)

        # if user is found, fail
        if user is not None:
            # escaping is done in template
            return render_template("error.html", error="Account for %s already exists" % request.form["email"])

        # add user to users table, and log in
        id = r.model.user.create(request.form['name'], request.form['email'], request.form['password'])
        session['user_id'] = id
        return redirect(url_for('home'))

    # show register form on GET
    else:
        return render_template('pages/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Logs in the user with provided name and password (or shows login form). """

    # perform login on POST
    if request.method == 'POST':
        # if email or password not provided, fail
        if request.form['email'] == '' or request.form['password'] == '':
            return render_template("error.html", error="Please enter an email address and password.")

        # else, look for email in db
        user = r.model.user.get_by_email(request.form['email'], filter=False)

        # if no user found, fail
        if user is None:
            # escaping is done in template
            return render_template("error.html", error="No account for %s found" % request.form["email"])

        # check if password correct
        elif check_password_hash(user['password'], request.form['password']):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            return render_template("error.html", error="Invalid password.")

    # show login form on GET
    else:
        return render_template('pages/login.html')

@app.route('/logout', methods=['GET'])
def logout():
    """ Log out the current user. """

    session.clear()
    return redirect(url_for('home'))

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    """ User profile page. """

    user = r.model.user.get_by_username(username)
    uploads = r.model.upload.Upload.get_where({'user_id': user.id})
    comments = r.model.comment.Comment.get_where({'user_id': user.id})
    files = r.model.file.File.get([e.file_id for e in comments.values()])

    upload_count = r.model.upload.Upload.get_count_where({'user_id': user.id})
    comment_count = r.model.comment.Comment.get_count_where({'user_id': user.id})

    return render_template('profile.html', uploads=uploads, upload_count=upload_count, comment_count=comment_count,
        line_count=123, user=user)
