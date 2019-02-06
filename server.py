"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/register', methods=["GET"])
def register_form():
    
    # # Process registration form, 
    # email_address = request.form.get('email')
    # password = request.form.get('password')

    # #check if user with email address exists.
    # addresses = User.query.filter_by(email=email_address).all()

    # # If not, create a new user in the database.
    # if addresses == []:
    #     User(email_address, password)
    #     db.session.commit()
    # else:
    #     # Flash message
    #     flash('That email address has already been used')
    #     return redirect('register_form.html')

    return render_template('register_form.html')

@app.route('/register', methods=["POST"])
def register_process():

    # Process registration form, 
    email_address = request.form.get('email')
    password = request.form.get('password')

    #check if user with email address exists.
    addresses = User.query.filter_by(email=email_address).all()

    # If not, create a new user in the database.
    if email_address == '':
        flash('Please enter an email address')
        return redirect('/register')

    elif addresses == []:
        User(email_address, password)
        db.session.commit()
    else:
        # Flash message
        flash('That email address has already been used')
        return redirect('/register')

    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
