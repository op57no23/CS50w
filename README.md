# Project 1

Web Programming with Python and JavaScript

This site provides users the ability to search a database of books and to leave reviews for them. It retrieves information from the GoodReads API and has it's own api route. The contents of each file are detailed below: 

## Templates

### login.html
This page has a form that posts to the index route for login and a link to the registration page. If the password provided is incorrect or the user has succesfully logged out, an alert message will be shown.

### layout.html
The parent page of the home, book, and search pages. It has a navbar that allows users to logout and return to the home page and has space for a block title and a block body.

### register.html
A form to register a new user. Upon submission, the user will be added to the database if they are unique and then the user will be redirected to the login page and asked to login.

### home.html
The page displays all the reviews that the user has entered and provides a search tool.

### search.html
The page displays all the results of the search from the home.html page.

### book.html
After clicking on a link to a book on the search page, the user is directed to the book page which displays information about the book, including information pulled from the goodreads api, displays the reviews that have been left for that title, and provides a form for the user to add a review. 

## Application

### application.py
The main application file handles all the form info and database entries, search queries, and error handling. It relays template information to the html pages and handles user sessions and password encryption and verification. If the user requests the route /api/<isbn> the application will return a json object with the information from the site.

### import.py
This file reads the provided csv of book titles into the database.

### requirements.text
A listing of python modules that must be installed to run the app.
