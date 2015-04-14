from flask import request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import r
from r import app

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Register user. """

    # create new user on POST
    if request.method == 'POST':
        # if email or passwords not provided, fail
        if request.form['name'] == '' or request.form['email'] == '' or request.form['password'] == '' or request.form['password2'] == '':
            return r.renderer.page("error.html", error="Please enter an email address and password.")

        # make sure passwords match
        if request.form['password'] != request.form['password2']:
            return r.renderer.page("error.html", error="Passwords must match.")

        # else, look for email in db
        user = r.model.user.get_by_email(request.form['email'], filter=False)

        # if user is found, fail
        if user is not None:
            return r.renderer.page("error.html", error="Account for %s already exists" % request.form["email"])

        # add user to users table, and log in
        id = r.model.user.create(request.form['name'], request.form['email'], request.form['password'])
        session['user_id'] = id
        return redirect(url_for('home'))

    # show register form on GET
    else:
        return r.renderer.page('pages/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Logs in the user with provided name and password (or shows login form). """

    # perform login on POST
    if request.method == 'POST':
        # if email or password not provided, fail
        if request.form['email'] == '' or request.form['password'] == '':
            return r.renderer.page("error.html", error="Please enter an email address and password.")

        # else, look for email in db
        user = r.model.user.get_by_email(request.form['email'], filter=False)

        # if no user found, fail
        if user is None:
            return r.renderer.page("error.html", error="No account for %s found" % request.form["email"])

        # check if password correct
        elif check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect('/')
        else:
            return r.renderer.page("error.html", error="Invalid password.")

    # show login form on GET
    else:
        return r.renderer.page('pages/login.html')

@app.route('/logout', methods=['GET'])
def logout():
    """ Log out the current user. """

    session.clear()
    return redirect(url_for('home'))

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    """ User profile page. """

    user = r.model.user.get_by_username(username)
    uploads = r.model.upload.uploads_for_feed(user.id)
    reviews = r.model.upload.reviews_for_feed(user.id)

    upload_count = r.model.upload.Upload.get_count_where({'user_id': user.id})
    comment_count = r.model.comment.Comment.get_count_where({'user_id': user.id})

    # TODO: change to a model function/query, since this won't work
    # once we paginate
    file_count = sum(len(upload.files) for upload in uploads.values())
    line_count = sum(upload._line_count for upload in uploads.values())

    return r.renderer.page(
        'pages/profile.html',
        uploads=uploads,
        reviews=reviews,
        upload_count=upload_count,
        comment_count=comment_count,
        line_count=line_count,
        file_count=file_count,
        user=user
    )
