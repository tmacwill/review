from review import app, db
import review.model.user as user_model
from flask import render_template, request, session
import crypt

# logs in the user with provided name and password (or shows login form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # perform the login
    if request.method == "POST":
        #if email or password not provided, fail
        # else, look for email in db
        user = user_model.get({"email": request.form["email"]}, one=True)
        # if no user found, fail
        if user is None:
            # XXX need to escape?
            return render_template("error.html", error="No account for %s found" % request.form["email"])
        else:
            if user["password"] == crypt.crypt(request.form["password"], user["password"]):
                session["user_id"] = user["id"]
                return render_template("home.html", user=session["user_id"])
            else:
                return render_template("error.html", error="Invalid password.")
    else:
        return render_template("login.html")


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()

