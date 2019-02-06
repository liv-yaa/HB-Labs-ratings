"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
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


@app.route('/users/<int:user_id>')
def user_info(user_id):
    """ Show list of movies from one user given user id."""

    movies = db.session.query(User.user_id)

    user = User.query.get(user_id)
    ratings = Rating.query.filter_by(user_id=user.user_id).all()
    # movies = []

    # for r in ratings:
    #     movie = Movie.query.get(r.movie_id)
    #     movies.append(movie)


    return render_template('user_info.html', user=user, ratings=ratings)


@app.route('/register', methods=["GET"])
def register_form():
    """ """

    return render_template('register_form.html')


@app.route('/register', methods=["POST"])
def register_process():
    """ """

    # Process registration form, 
    email_address = request.form.get('email')
    password = request.form.get('password')

    # check if user with email address exists.
    addresses = User.query.filter_by(email=email_address).all()

    # If not, create a new user in the database.
    if email_address == '':
        flash('Please enter an email address')
        return redirect('/register')

    elif addresses == []:
        new_user = User(email=email_address, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.email
        flash(f"Logged in as {email_address}.")
        return redirect('/')


    else:
        # Flash message
        flash('That email address has already been used')
        return redirect('/register')

    return redirect('/login')

@app.route('/login', methods=["GET"])
def login_form():
    """ Get method for the route that handles submission of the login form. """

    return render_template('login_form.html')

@app.route('/login', methods=["POST"])
def login_process():
    """ """
    
    # Process registration form, 
    email_address = request.form.get('email')
    typed_password = request.form.get('password')

    # check if user with email address exists.
    login_user = User.query.filter_by(email=email_address, 
                                    password=typed_password).first()

    # print(login_user)


    # If the user correctly logs in.
    if login_user:
        session['user'] = login_user.email
        flash(f"Logged in as {email_address}.")
        return redirect('/')


    else:
        # Flash message
        flash('That does not match any email-password combinations in our database.')
        return redirect('/login')

    # return redirect('/')

@app.route('/logout', methods=["POST"])
def logout_process():
    """ """

    # If the user is already logged in.
    if session['user']:
        # Set the user from the session to None:
        session['user'] = None
        flash(f"Logged out.")
        return redirect('/')


    else:
        # Flash message
        flash('No one is logged in currently.')
        return redirect('/login')



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
