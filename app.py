from flask import Flask, render_template, request, redirect, session

import login
import mta
import sms

app = Flask(__name__)


@app.route("/")
def home():
    # return render_template("home.html")
    return statusPage()


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

    # separate the lines for styling
    D = {'red': [],
         'green': [],
         'purple': [],
         'blue': [],
         'orange': [],
         'gtrain': [],
         'grey': [],
         'brown': [],
         'yellow': [],
         'color': []}

    red = ["1", "2", "3"]
    green = ["4", "5", "6"]
    purple = ["7"]
    yellow = ["N", "Q", "R"]
    blue = ["A", "C", "E"]
    orange = ["B", "D", "F", "M"]
    gtrain = ["G"]
    grey = ["L", "S"]
    brown = ["J", "Z"]

    for delay in service.delays:
        if delay.line in red:
            D['red'].append(delay.line)
            red.remove(delay.line)
        elif delay.line in green:
            D['green'].append(delay.line)
            green.remove(delay.line)
        elif delay.line in purple:
            D['purple'].append(delay.line)
            purple.remove(delay.line)
        elif delay.line in blue:
            D['blue'].append(delay.line)
            blue.remove(delay.line)
        elif delay.line in orange:
            D['orange'].append(delay.line)
            orange.remove(delay.line)
        elif delay.line in gtrain:
            D['gtrain'].append(delay.line)
            gtrain.remove(delay.line)
        elif delay.line in grey:
            D['grey'].append(delay.line)
            grey.remove(delay.line)
        elif delay.line in brown:
            D['brown'].append(delay.line)
            brown.remove(delay.line)
        elif delay.line in yellow:
            D['yellow'].append(delay.line)
            yellow.remove(delay.line)
        else:
            D['color'].append(delay.line)

    D2 = {'red': red,
          'green': green,
          'purple': purple,
          'blue': blue,
          'orange': orange,
          'gtrain': gtrain,
          'grey': grey,
          'yellow': yellow,
          'brown': brown}

    return render_template("status.html", service=service, colors=D, running=D2)


def handleRedirect(redirectPage="/"):
    if "nextpage" in session:
        n = session["nextpage"]
        session.pop("nextpage")
    else:
        n = redirectPage

    return redirect(n)


@app.route("/sms/receive",methods=["GET","POST"])
def test():
	if request.method=="GET":
		sms.send_message("hello there",9174350162)
	if request.method=="POST":
            print "haven't set up receiving messages yet"



def main():
    app.secret_key = "very secret"
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
