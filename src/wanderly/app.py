from flask import (
    Flask,
    flash,
    g,
    render_template,
    redirect,
    request,
    session,
    url_for
)

from filters import (
    safe_default, 
    formatted_date,
    formatted_title_date,
    formatted_time
    )
from utils import (
    error_for_trips,
)

from functools import wraps
import bcrypt
import secrets
from database import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

app.jinja_env.filters['safe_default'] = safe_default
app.jinja_env.filters['formatted_date'] = formatted_date
app.jinja_env.filters['formatted_title_date'] = formatted_title_date
app.jinja_env.filters['formatted_time'] = formatted_time

def valid_credentials(email, password):
    user = g.storage.get_user_credentials(email)
    if user:
        stored_password = user["password"].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return user
    return None

def user_logged_in():
    return 'user_id' in session

def require_logged_in_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not user_logged_in():
            flash("Please sign for access.", "info")
            return redirect(url_for('show_login_form'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_db():
    g.storage = Database()

@app.route("/")
@require_logged_in_user
def index():
    return redirect(url_for('show_trips'))

@app.route("/login")
def show_login_form():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    user = valid_credentials(email, password)
    if user:
        session['user_id'] = user['id']
        return redirect(url_for('index'))
    else:
        flash("Invalid credentials", "error")
        return render_template("login.html"), 401

@app.route("/signup")
def show_signup_form():
    return render_template("signup.html")

@app.route("/trips")
@require_logged_in_user
def show_trips():
    trips = g.storage.get_trips_by_user(session['user_id'])
    name = g.storage.get_name_by_id(session['user_id'])['full_name']
    if name:
        first_name = name.split()[0]
    return render_template("trips.html", trips=trips, first_name=first_name)

@app.route("/trips", methods=["POST"])
@require_logged_in_user
def create_trip():
    destination = request.form['destination'].strip()
    start_date = request.form['start-date']
    end_date = request.form['end-date']

    error = error_for_trips(destination, start_date, end_date)
    if error:
        flash(error, "error")
        return render_template("create_trip.html", destination=destination, start_date=start_date, end_date=end_date)

    g.storage.create_new_trip(destination, start_date, end_date, session['user_id'])
    flash('Your new adventure has been created', "success")
    return redirect(url_for('index'))

@app.route("/trips/<int:trip_id>")
@require_logged_in_user
def trip_schedule(trip_id):
    trip = g.storage.find_trip_by_id(trip_id)
    schedule = g.storage.get_itinerary(trip_id)
    plans_by_date = {}

    for activity in schedule: 
        date = activity['activity_date']

        if date not in plans_by_date:
            plans_by_date[date] = []

        plans_by_date[date].append(activity)

    return render_template("itinerary.html", plans_by_date=plans_by_date, trip=trip)

@app.route("/trips/<int:trip_id>", methods=['POST'])
@require_logged_in_user
def delete_trip(trip_id):
    g.storage.delete_trip_by_id(trip_id)
    flash("The trip has been deleted", "success")
    return redirect(url_for('index'))

@app.route("/trips/new")
@require_logged_in_user
def plan_new_trip():
    return render_template("create_trip.html")

@app.route("/signout", methods=["POST"])
@require_logged_in_user
def signout():
    session.clear()
    flash("You have been signed out", "success")
    return redirect(url_for('show_login_form'))

if __name__ == "__main__":
    app.run(debug=True, port=5003)