import os
from passlib.hash import pbkdf2_sha256
import pdb

import logging
logging.basicConfig(filename = 'app.log', level = logging.DEBUG)

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("login.html", incorrect_password = False)


@app.route("/home", methods = ["POST"])
def home():
#register request
    if (len(request.form) == 4):
        first = request.form.get('first_name')
        last = request.form.get('last_name')
        email = request.form.get("email")
        password = pbkdf2_sha256.hash(request.form.get("password"))
        db.execute("INSERT INTO users (id, first, last, email, password) VALUES (DEFAULT, :first, :last, :email, :password)", {"first": first, "last": last, "email": email, "password": password})
        db.commit()

#login attemp
    if (len(request.form) == 2):
        try:
            result = db.execute("SELECT password from users WHERE email = :email", {"email": request.form.get("email")})
            hash = result.first()['password']
        except TypeError:
            return render_template("login.html", user_not_registered = True)

        #incorrect password
        if pbkdf2_sha256.verify(request.form.get("password"), hash) == False:
            return render_template("login.html", incorrect_password = True)
    result = db.execute("SELECT first FROM users WHERE email = :email", {"email": request.form.get("email")})
    user = result.first()['first']
    return render_template("home.html", user = user)

@app.route("/register", methods = ["GET"])
def register():
    return render_template("register.html")
