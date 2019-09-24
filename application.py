import os
from passlib.hash import pbkdf2_sha256
import pdb
import requests

from flask import Flask, session, render_template, request, url_for, redirect, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
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


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == 'POST': 
        #register request
        first = request.form.get('first_name')
        last = request.form.get('last_name')
        username = request.form.get("username")
        password = pbkdf2_sha256.hash(request.form.get("password"))
        try:
            db.execute("INSERT INTO users (id, first, last, username, password) VALUES (DEFAULT, :first, :last, :username, :password)", {"first": first, "last": last, "username": username, "password": password})
            db.commit()
            return render_template("login.html", succesful_register = True)
        except IntegrityError:
            flash("Looks like that username is already registered. Please login or register a new username.")
            return redirect(url_for('register'))


    if 'username' in session:
        return redirect(url_for('home'))

    return render_template("login.html")


@app.route("/home", methods = ["GET","POST"])
def home():
    if request.method == "GET":
        if 'username' not in session:
            return redirect(url_for("index"))

   #login attemp
    if request.method == "POST":
        try:
            result = db.execute("SELECT password from users WHERE username = :username", {"username": request.form.get("username")})
            hash = result.first()['password']
        except TypeError:
            flash("You are not registered. Please do so.")
            return render_template("login.html")

        #incorrect password
        if pbkdf2_sha256.verify(request.form.get("password"), hash) == False:
            flash("Your password does not match what is on file. Please try again")
            return redirect(url_for('index'))
        else:
            session['username'] = request.form.get("username")
    result = db.execute("SELECT first, id FROM users WHERE username = :username", {"username": session['username']})
    user = result.first()
    reviews = db.execute("select stars, review, title from reviews join books on books.id = reviews.book_id where user_id = :user_id ", {"user_id": user['id']}).fetchall()
    return render_template("home.html", user = user['first'], reviews = reviews)

@app.route("/register", methods = ["GET"])
def register():
    return render_template("register.html")

@app.route("/search" , methods = ["POST"])
def search():
    types = {'1': "isbn", '2': "title", '3': "author"}
    searchtype = types[request.form.get("searchType")]
    search = request.form.get("query")
    if (request.form.get("searchType") != '1'):
        search = search.lower()
        result = db.execute("SELECT * FROM books WHERE LOWER(books."+ searchtype + ") LIKE '%" + search + "%'").fetchall()
    else:
        result = db.execute("SELECT * FROM books WHERE books."+searchtype + " LIKE '%" + search + "%'").fetchall()
    if len(result) == 0:
        flash("Your search didn't turn up any matches. Please try another search")
        return redirect(url_for('home'))
    return render_template("search.html", result = result)

@app.route("/api/<string:isbn>")
def api(isbn):
    book_info = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).first()
    review_count = db.execute("select count(review) from reviews join books on books.id = reviews.book_id where isbn = :isbn", {"isbn": isbn}).first()
    average_stars = db.execute("select avg(stars) from reviews join books on books.id = reviews.book_id where isbn = :isbn", {"isbn": isbn}).first()
    return jsonify(title = book_info['title'], author = book_info['author'], year = book_info['year'], isbn = book_info['isbn'], review_count = review_count['count'], average_score = str(average_stars['avg']))


@app.route("/search/<string:isbn>", methods = ["GET", "POST"])
def book(isbn):
    if (request.method == "POST"):
        book_id = db.execute("select id from books where isbn=:isbn", {"isbn": isbn}).fetchone()[0]
        user_id = db.execute("select id from users where username=:username", {"username": session.get('username')}).fetchone()[0]
        already_submitted = db.execute("select count(review) from reviews join users on users.id = reviews.user_id join books on books.id = reviews.book_id where isbn=:isbn and user_id = :user_id", {"user_id": user_id, "isbn": isbn}).fetchone()['count'] > 0
        if not already_submitted:
            db.execute("insert into reviews (id, stars, review, book_id, user_id) values (DEFAULT, :stars, :review, :book_id, :user_id);", {"stars": request.form.get("stars"), "review": request.form.get("review_text"), "book_id": book_id, "user_id": user_id})
            db.commit() 
        if already_submitted:
            flash("Looks like you have already left a review for this book. Please select another book to review")
    book = db.execute("SELECT * FROM books WHERE books.isbn=:isbn", {"isbn": isbn}).fetchone()
    reviews = db.execute("select stars, review, first, last from reviews join books on books.id = reviews.book_id join users on users.id = reviews.user_id where isbn=:isbn;", {"isbn": isbn}).fetchall()
    good_reads = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"key": "amTBWEPOTackbMtDLQ9Drg", "isbns": isbn}).json()
    return render_template("book.html", book = book, reviews = reviews, good_reads = good_reads)

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("You have succesfully logged out")
    return redirect(url_for('index')) 
