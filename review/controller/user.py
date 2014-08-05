import review.model.user
from review import app, db
from flask import render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

# register user
@app.route('/register', methods=['GET', 'POST'])
def register():
    # perform the registration
    if request.method == "POST":
        #if email or passwords not provided, fail
        if request.form["name"] == '' or request.form["email"] == '' or request.form["password"] == '' or request.form["password2"] == '':
            return render_template("error.html", error="Please enter an email address and password.")

        # make sure passwords match
        if request.form["password"] != request.form["password2"]:
            return render_template("error.html", error="Passwords must match.")

        # else, look for email in db
        user = review.model.user.get({"email": request.form["email"]}, one=True)

        # if user is found, fail
        if user is not None:
            # escaping is done in template
            return render_template("error.html", error="Account for %s already exists" % request.form["email"])

        # add user to users table, and log in
        id = review.model.user.add(request.form["name"], request.form["email"], request.form["password"])
        session["user_id"] = id

        return redirect(url_for('home'))
    else:
        return render_template("register.html")

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
