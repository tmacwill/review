import review.model.user
from review import app, db
from flask import render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

# logs in the user with provided name and password (or shows login form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # perform the login
    if request.method == "POST":
        # if email or password not provided, fail
        if request.form["email"] == '' or request.form["password"] == '':
            return render_template("error.html", error="Please enter an email address and password.")

        # else, look for email in db
        user = review.model.user.get({"email": request.form["email"]}, one=True)
        # if no user found, fail
        if user is None:
            # escaping is done in template
            return render_template("error.html", error="No account for %s found" % request.form["email"])

        # check if password correct
        elif check_password_hash(user["password"], request.form["password"]):
            session["user_id"] = user["id"]
            return redirect(url_for('home'))
        else:
            return render_template("error.html", error="Invalid password.")
    else:
        return render_template("login.html")


# logs out the current user
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))

# default for now. should be in different controller
@app.route('/')
def home():
    # pull user from session
    user = session.get("user_id", None)
    return render_template("home.html", user=user)
