import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute(
        "SELECT stock_name, symbol, SUM(number) AS stocks FROM history WHERE user_id = ? GROUP BY symbol HAVING SUM(number) != 0", session["user_id"])
    total = 0
    i = 0
    for stock in portfolio:
        quote = lookup(stock["symbol"])
        if quote == None:
            return apology(f"{stock['symbol']} cannot be found in IEX database")
        stock["price"] = quote["price"]
        total += stock["price"] * stock["stocks"]
        i += 1
    cash = db.execute("SELECT cash FROM users WHERE id is ?", session["user_id"])[0]
    cash = cash["cash"]
    return render_template("index.html", stocks=portfolio, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST to submit registration (as by submitting a form via POST)
    if request.method == "POST":
        # Check if form is filled
        if request.form.get("symbol") == "" or request.form.get("shares") == "" or request.form.get("symbol") == None or request.form.get("shares") == None:
            return apology("Enter a symbol and number of shares")
        # check if number of shares is larger than 0
        try:
            shares = float(request.form.get("shares"))
            if not shares.is_integer():
                return apology("You cannot buy fractional stocks")
        except ValueError:
            return apology("You did not provide a numer")
        if shares < 0:
            return apology("Number must be greater or equal to 1")
        # get share info from IEX and process it
        quote = lookup(request.form.get("symbol"))
        if quote != None:
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]
            cash = cash["cash"]
            if cash < float(quote["price"]) * shares:
                return apology("Not enough cash")
            new_cash = cash - float(quote["price"]) * shares
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, stock_name, price, number) VALUES (?, ?, ?, ?, ?)",
                       session["user_id"], quote["symbol"], quote["name"], quote["price"], shares)
            return redirect("/")
        # apology if share symbol is not in IEX database
        else:
            return apology("Symbol not found in IEX database")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change the password of the logged in user"""
    # User reached route via POST to submit registration (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("old_password"):
            return apology("Must provide old password")

        # Check old password
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("Old password incorrect")

        # Ensure password was submitted
        elif not request.form.get("new_password"):
            return apology("Must provide new password")

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("Must repeat password")

        # Ensure passwords match
        elif request.form.get("new_password") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        # Insert new user in users table of finance database
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(request.form.get("new_password")), session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute(
        "SELECT stock_name, symbol, number, price, time FROM history WHERE user_id = ? ORDER BY time", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST to submit registration (as by submitting a form via POST)
    if request.method == "POST":
        if request.form.get("symbol") == "":
            return apology("Enter a symbol")
        quote = lookup(request.form.get("symbol"))
        if quote != None:
            return render_template("quoted.html", quote=quote)
        else:
            return apology("Symbol not found in IEX database")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST to submit registration (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Check if user already exists
        if db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            return apology("Username already taken")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("Must repeat password")

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        # Insert new user in users table of finance database
        session["user_id"] = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                                        request.form.get("username"), generate_password_hash(request.form.get("password")))

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    portfolio = db.execute(
        "SELECT stock_name, symbol, SUM(number) AS stocks FROM history WHERE user_id is ? GROUP BY symbol HAVING SUM(number) != 0", session["user_id"])
    # User reached route via POST to submit registration (as by submitting a form via POST)
    if request.method == "POST":
        # Check if form is filled
        if request.form.get("symbol") == "" or request.form.get("shares") == "":
            return apology("Enter a symbol and number of shares", 403)
        # check if number of shares is larger than 0
        shares = int(request.form.get("shares"))
        if shares < 0:
            return apology("Number must be greater or equal to 1", 402)
        # check if user has enough shares
        stock = None
        for s in portfolio:
            if s["symbol"] == request.form.get("symbol"):
                stock = s
        if stock == None:
            return apology("You do not own this stock")
        if stock["stocks"] < shares:
            return apology(f"You do not have enough shares of {stock['stock_name']}")
        # get share info from IEX and process it
        quote = lookup(request.form.get("symbol"))
        if quote != None:
            # update cash of the user
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]
            cash = cash["cash"]
            new_cash = cash + float(quote["price"]) * shares
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
            # update stocks
            db.execute("INSERT INTO history (user_id, symbol, stock_name, price, number) VALUES (?, ?, ?, ?, ?)",
                       session["user_id"], quote["symbol"], quote["name"], quote["price"], -1 * shares)
            return redirect("/")
        # apology if share symbol is not in IEX database
        else:
            return apology("Symbol not found in IEX database", 404)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", portfolio=portfolio)
