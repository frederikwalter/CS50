import os
import requests

from datetime import datetime
from flask import render_template, redirect, session
from functools import wraps

def error(message, code=400):
    """Render message as an error to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code


# Check if user is logged in - otherwise redirect to login page
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Calculate and nicely format timedelta
def format_time(timestamp):
    # format the elapsed time output
    timestamp = datetime.strptime(timestamp.split(".")[0], '%Y-%m-%d %H:%M:%S')

    elapsed_time = datetime.now() - timestamp
    if elapsed_time.days > 0:
        if elapsed_time.days == 1:
            return f"Vor einem Tag"
        else:
            return f"Vor {elapsed_time.days} Tagen"
    elif elapsed_time.seconds >= 3600:
        hours = elapsed_time.seconds // 3600
        if hours == 1:
            return "Vor einer Stunde"
        else:
            return f"Vor {hours} Stunden" 
    else:
        minutes = elapsed_time.seconds // 60
        if minutes == 1:
            return "Vor einer Minute"
        else:
            return f"Vor {minutes} Minuten" 