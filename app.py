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
    return "hello"

@app.route("/login")
def login():
    pass

@app.route("/logout")
def logout():
    pass

@app.route("/register")
def register():
    pass

@app.route("/manage_account")
def manageAccount():
    pass

def main():
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
