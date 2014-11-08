from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

import login

app = Flask(__name__)


@app.route("/")
def home():
    loggedIn = False
    username = ""
    if "user" in session:
        loggedIn = True
        username = session["user"]

    # pass in values of username so that it shows up in navbar
    return render_template("home.html", username=username, loggedIn=loggedIn)


@app.route("/login", methods=["GET", "POST"])
def loginPage():
    if "user" in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")
    else:
        fieldUsername = request.form["username"]
        fieldPassword = request.form["password"]

        success = login.login(fieldUsername, fieldPassword)

        if success:
            session["user"] = fieldUsername
            return handleRedirect()
        else:
            flash("Login Invalid")
            return render_template("login.html", loggedIn=False)


@app.route("/logout")
def logoutPage():
    if "user" in session:
        username = session["user"]
        password = session["password"]

        login.logout(username, password)
        session.pop("user")
    return handleRedirect()


@app.route("/register")
def registerPage():
    if "user" in session:
        return handleRedirect()
    if request.method == "GET":
        return render_template("register.html")
    else:
        fieldUsername = request.form["username"]
        fieldPhone = request.form["phone"]
        fieldPassword = request.form["password"]

        success = login.addUser(fieldUsername, fieldPassword)

        if success:
            session["user"] = fieldUsername
            handleRedirect()
        else:
            flash("Email already exists")
            return render_template("register.html")


@app.route("/manage_account/<username>")
def manageAccountPage(username):
    pass


def handleRedirect(redirectPage="/"):
    if "nextpage" in session:
        n = session["nextpage"]
        session.pop("nextpage")
    else:
        n = redirectPage

    return redirect(n)


def main():
    app.secret_key = "very secret"
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
