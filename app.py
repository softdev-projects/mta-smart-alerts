from flask import Flask, render_template, request, redirect, session

import login
import mta
import sms

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def loginPage():
    if "user" in session:
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html")

    errors = {"invalid login": "Login invalid"}

    fieldUsername = request.form["username"]
    fieldPassword = request.form["password"]

    success = login.login(fieldUsername, fieldPassword)

    if success:
        session["user"] = fieldUsername
        return handleRedirect()
    else:
        error = errors["invalid login"]
        return render_template("login.html",
                               error=error,
                               loggedIn=False)


@app.route("/logout")
def logoutPage():
    if "user" in session:
        username = session["user"]

        login.logout(username)
        session.pop("user")
    return handleRedirect()


@app.route("/register", methods=["GET", "POST"])
def registerPage():
    if "user" in session:
        return handleRedirect()

    errors = {"user-exists": "Email already exists",
              "phone-exists": "Phone number already exists",
              "password-short": "Password is too short"}
    if request.method == "GET":
        return render_template("register.html")
    else:
        fieldUsername = request.form["username"]
        fieldPhone = request.form["phone"]
        fieldPassword = request.form["password"]

        success = login.addUser(fieldUsername, fieldPassword, fieldPhone)

        if success:
            session["user"] = fieldUsername
            handleRedirect()
        else:
            error = errors["user-exists"]
            return render_template("register.html", error=error)


@app.route("/manage_account")
@app.route("/manage_account/<username>")
def manageAccountPage(username):
    if "user" not in session:
        session["nextpage"] = "/manage_account"
        return redirect("/login")
    if "user" in session:
        accountSettings = {}
        # accountSettings = db.getAccountSettings(session["user"])
        return render_template("account_settings.html", accountSettings)


@app.route("/status")
def statusPage():
    service = mta.service_status()
    return render_template("status.html", service=service)


def handleRedirect(redirectPage="/"):
    if "nextpage" in session:
        n = session["nextpage"]
        session.pop("nextpage")
    else:
        n = redirectPage

    return redirect(n)


@app.route("/twilio/receive",methods=["GET","POST"])
def test():
	if request.method=="GET":
		twilio.send_message()
	if request.method=="POST":
            print "haven't set up receiving messages yet"



def main():
    app.secret_key = "very secret"
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
