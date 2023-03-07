import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mateofmath.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    """Show The Formula"""
    formulas = db.execute("SELECT images,volume_perimeter,surface_area FROM geo_form WHERE category='3D'")
    formulas2 = db.execute("SELECT images,volume_perimeter,surface_area FROM geo_form WHERE category='2D'")

    return render_template("home.html", formulas=formulas, formulas2=formulas2)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not email:
            return apology('Email is required!')
        elif not password:
            return apology('Password is required!')
        elif not confirmation:
            return apology('Confirmation Password is required!')

        if password != confirmation:
            return apology('Password does not match!')

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (email,password) VALUES (?, ?)", email, hash)
            return redirect('/')
        except:
            return apology('Email has already been registered!')
    else:
        return render_template("register.html")

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    """Contact Us"""
    if (request.method == "POST"):
        email = request.form.get('email')
        topic = request.form.get('topic')
        desc = request.form.get('desc')

        if not email:
            return apology('Email is required!')

        db.execute("INSERT INTO contact (email, topic, desc) VALUES (?,?,?)", email, topic, desc)
        return redirect('/')
    else:
        return render_template("contact.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")

@app.route("/square", methods=["GET", "POST"])
def square():
    return render_template("square.html")

@app.route("/rectangle", methods=["GET", "POST"])
def rectangle():
    return render_template("rectangle.html")

@app.route("/triangle", methods=["GET", "POST"])
def triangle():
    return render_template("triangle.html")

@app.route("/paralellogram", methods=["GET", "POST"])
def paralellogram():
    return render_template("paralellogram.html")

@app.route("/circle", methods=["GET", "POST"])
def cirle():
    return render_template("circle.html")

@app.route("/kite", methods=["GET", "POST"])
def kite():
    return render_template("kite.html")

@app.route("/trapezoid", methods=["GET", "POST"])
def trapezoid():
    return render_template("trapezoid.html")


@app.route("/spare", methods=["GET", "POST"])
@login_required
def spare():
    return render_template("spare.html")

@app.route("/cube", methods=["GET", "POST"])
@login_required
def cube():
    return render_template("cube.html")

@app.route("/cylinder", methods=["GET", "POST"])
@login_required
def cylinder():
    return render_template("cylinder.html")

@app.route("/cone", methods=["GET", "POST"])
@login_required
def cone():
    return render_template("cone.html")

@app.route("/beam", methods=["GET", "POST"])
@login_required
def beam():
    return render_template("beam.html")

if __name__ == '__main__':
    app.run(debug=True)