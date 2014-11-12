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

    # separate the lines into delayed and normal for styling
    delayed_lines = []
    line_colors = {'123': 'red', '456': 'green', '7': 'purple', 'ACE': 'blue',
                   'BDFM': 'orange', 'G': 'g_line', 'JZ': 'brown',
                   'L': 'l_line', 'NQR': 'yellow', 'S': 's_shuttle',
                   'SIR': 'si_railway'}

    for delay in service.delays:
        for line, color in line_colors.iteritems():
            if delay.line == line:
                delayed_lines.append([line, color])
                del line_colors[line]

    print delayed_lines
    print line_colors
    return render_template("status.html", service=service,
                           delayed_lines=delayed_lines, running=line_colors)


@app.route("/status_fake")
def status_page_fake():
    with open("test/no_delay.xml") as f:
        fake_xml = f.read()

    print fake_xml
    service = mta.MTASubwayStatus(fake_xml)
    return render_template("status.html", service=service)


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
