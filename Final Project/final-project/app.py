import os

from datetime import datetime
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from helpers import error, login_required, format_time
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
# create an engine to connect to your database
db = create_engine('sqlite:///autostopp.db')


# Index route for hello world application
@app.route("/")
@login_required
def hello_world():
    """Get to login page for now"""
    return redirect("/feed")


@app.route('/challenges', methods =["GET", "POST"])
@login_required
def challenges():
    if request.method == "POST" and request.form.get("sort") == "bonus":
        challenges_list = db.execute("SELECT id, name, bonus, description, link FROM challenges ORDER BY bonus").fetchall()
    else:
        challenges_list = db.execute("SELECT id, name, bonus, description, link FROM challenges ORDER BY name").fetchall()
    
    return render_template("challenges.html", challenges_list=challenges_list, name=session["user_name"])
        


# Handle completion of challenges
@app.route('/complete_challenge', methods =["POST"])
@login_required
def complete_challenge():
    challenge_id = request.form.get("challenge_id")
    location = request.form.get("location")
    notes = request.form.get("notes")

    # Check if user has already completed challenge
    user_id = session["user_id"]
    existing_record = db.execute("SELECT * FROM completed_challenges WHERE user_id = ? AND challenge_id = ?", user_id, challenge_id).fetchone()
    if existing_record:
        return error("You have already completed this challenge.")

    # Insert new record into completed_challenges table
    timestamp = datetime.now()
    db.execute("INSERT INTO completed_challenges (challenge_id, user_id, location, notes, timestamp) VALUES (?, ?, ?, ?, ?)", challenge_id, user_id, location, notes, timestamp)

    return redirect("/challenges")   


# Display feed 
@app.route('/feed')
@login_required
def feed():
    feed_elements = db.execute("SELECT completed_challenges.id AS id, users.name AS user_name, challenges.name AS challenge_name, challenges.bonus AS bonus, challenges.link AS link, completed_challenges.location AS location, completed_challenges.notes AS notes, completed_challenges.timestamp AS timestamp FROM completed_challenges INNER JOIN users ON users.id = completed_challenges.user_id INNER JOIN challenges ON challenges.id = completed_challenges.challenge_id ORDER BY completed_challenges.timestamp DESC;").fetchall()
    feed_list = []
    for f in feed_elements:
        feed_list.append({"elapsed_time": format_time(f.timestamp), "feed": f})
    return render_template("feed.html", feed_list=feed_list, name=session["user_name"])


# Handle login of users
@app.route('/login', methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return error("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Query database for username
        result = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email")).fetchall()
        # Ensure username exists and password is correct
        if len(result) != 1 or not check_password_hash(result[0]["hash"], request.form.get("password")):
            return error("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = result[0]["id"]
        session["user_name"] = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"]).fetchone()[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route('/players')
@login_required
def players():    
    names = db.execute("SELECT users.id, users.name, COALESCE(SUM(challenges.bonus), 0) AS total_bonus FROM users LEFT JOIN completed_challenges ON users.id = completed_challenges.user_id LEFT JOIN challenges ON completed_challenges.challenge_id = challenges.id GROUP BY users.id ORDER BY total_bonus DESC;").fetchall()
    comp_challenges = []
    for name in names:
        temp = db.execute("SELECT completed_challenges.id, challenges.name AS c_name, bonus, description, link, notes, location, timestamp FROM completed_challenges JOIN challenges ON challenge_id = challenges.id WHERE user_id = ?", name.id).fetchall()
        comp_challenges.append({"id": name.id, "name": name.name, "total_bonus": name.total_bonus, "challenges": temp})
    
    return render_template("players.html", comp_challenges=comp_challenges, name=session["user_name"])


@app.route('/profile')
@login_required
def profile():
    return redirect("/")


# Register as a new user
@app.route('/register', methods=["GET", "POST"])
def register():
    # User reached route via POST to submit registration
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return error("Must provide email")

        # Check if user already exists
        result = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email")).fetchall()
        if len(result) != 0:
            return error("Email is already registered")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return error("Must repeat password")

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return error("Passwords do not match")
        
        # Insert new user in users table of finance database
        result = db.execute("INSERT INTO users (email, name, hash) VALUES(?, ?, ?)", request.form.get("email"), request.form.get("name"), generate_password_hash(request.form.get("password")))
        session["user_id"] = result.lastrowid
        session["user_name"] = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"]).fetchone()[0]

        return redirect("/")

    else:
        return render_template("register.html")