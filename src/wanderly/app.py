import bcrypt
from database import Database
from filters import (
    formatted_date,
    formatted_time,
    formatted_title_date,
    safe_default, 
    safe_default_money,
    )

from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from functools import wraps
from utils import (
    error_for_activity_input,
    error_for_create_user,
    error_for_login,
    error_for_trips,
    get_first_name,
    get_trip_heading,
    remove_punc_for_cost,
)

import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# ---- JINJA FILTERS ----
app.jinja_env.filters['formatted_date'] = formatted_date
app.jinja_env.filters['formatted_time'] = formatted_time
app.jinja_env.filters['formatted_title_date'] = formatted_title_date
app.jinja_env.filters['safe_default'] = safe_default
app.jinja_env.filters['safe_default_money'] = safe_default_money

# ---- AUTH HELPER FUNCTIONS ----
def valid_credentials(email, password):
    user = g.storage.get_user_credentials(email)
    if user:
        curr_password = password.encode('utf-8')
        stored_password = user["password"].encode('utf-8')
        if bcrypt.checkpw(curr_password, stored_password):
            return user
    return None


def user_logged_in():
    return 'user_id' in session


def require_logged_in_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not user_logged_in():
            session['next'] = request.full_path
            flash("Please sign for access.", "info")
            return redirect(url_for('show_login_form'))
        return f(*args, **kwargs)
    return decorated_function


# ---- BEFORE REQUEST -----
@app.before_request
def load_db():
    g.storage = Database()


# ---- AUTH ----
@app.route("/signup")
def show_signup_form():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def create_user():
    name = request.form['name'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    error = error_for_create_user(name, email, password)
    if error:
        flash(error, "error")
        return render_template("signup.html")
    
    if g.storage.user_exists(email):
        flash("The email is already in use.", "error")
        return render_template('signup.html')
    
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    g.storage.create_new_user(name, email, hash.decode('utf-8'))
    flash("User has been created", "success")
    return redirect(url_for('login'))


@app.route("/login")
def show_login_form():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    error = error_for_login(email, password)
    if error:
        flash(error, "error")
        return render_template('login.html')
    
    user = valid_credentials(email, password)

    if user:
        session['user_id'] = user['id']
        next_page = session.pop('next', None)
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)

    flash("Invalid credentials", "error")
    return render_template("login.html"), 401

@app.route("/signout", methods=["POST"])
@require_logged_in_user
def signout():
    session.clear()
    flash("You have been signed out", "success")
    return redirect(url_for('show_login_form'))


# ---- HOME ----
@app.route("/")
@require_logged_in_user
def index():
    return redirect(url_for('show_trips'))


@app.route("/trips")
@require_logged_in_user
def show_trips():
    trips = g.storage.get_trips_by_user_id(session['user_id'])
    first_name = get_first_name(trips, session['user_id'], g.storage)

    return render_template("trips.html", trips=trips, first_name=first_name)


@app.route("/trips/<int:trip_id>/edit", methods=["GET"])
@require_logged_in_user
def show_trip_to_edit(trip_id):
    trips = g.storage.get_trips_by_user_id(session['user_id'])
    first_name = get_first_name(trips, session['user_id'], g.storage)
    return render_template("trips.html", trips=trips, first_name=first_name, edit_trip_id=trip_id)


@app.route("/trips/<int:trip_id>/edit", methods=["POST"])
@require_logged_in_user
def edit_trip(trip_id):
    destination = request.form['destination'].strip()
    start_date = request.form['start_date'] or None
    end_date = request.form['end_date'] or None

    error = error_for_trips(destination, start_date, end_date)
    if error:
        flash(error, "error")
        return redirect(url_for('show_trip_to_edit', trip_id=trip_id))

    g.storage.edit_trip_heading(destination, start_date, end_date, trip_id)
    flash("Trip saved.", "success")
    return redirect(url_for('index'))


@app.route("/trips/<int:trip_id>", methods=['POST'])
@require_logged_in_user
def delete_trip(trip_id):
    g.storage.delete_trip_by_id(trip_id)
    flash("Trip deleted.", "success")
    return redirect(url_for('index'))


@app.route("/trips/new")
@require_logged_in_user
def plan_new_trip():
    return render_template("create_trip.html")


@app.route("/trips/new", methods=["POST"])
@require_logged_in_user
def create_trip():
    destination = request.form['destination'].strip()
    start_date = request.form['start-date'] or None
    end_date = request.form['end-date'] or None

    error = error_for_trips(destination, start_date, end_date)
    if error:
        flash(error, "error")
        return render_template("create_trip.html", destination=destination, start_date=start_date, end_date=end_date)

    g.storage.create_new_trip(destination, start_date, end_date, session['user_id'])
    flash('Your new adventure has been created!', "success")
    return redirect(url_for('index'))


# ---- ITINERARY ----
@app.route("/trips/<int:trip_id>")
@require_logged_in_user
def trip_schedule(trip_id):
    schedule = g.storage.get_itinerary(trip_id)
    trip = get_trip_heading(schedule, trip_id, g.storage)
    
    plans_by_date = {}
    for activity in schedule:
        date = activity['at_date'] or ""
        if date not in plans_by_date:
            plans_by_date[date] = []
        plans_by_date[date].append(activity)

    time = request.args.get("time", "")
    activity = request.args.get("activity", "")
    note = request.args.get("note", "")
    cost = request.args.get("cost", "")

    return render_template("itinerary.html", 
                           plans_by_date=plans_by_date, 
                           trip=trip,
                           time=time,
                           activity=activity,
                           note=note,
                           cost=cost,
                           )


@app.route("/trips/<int:trip_id>/activities/<int:activity_id>/edit", methods=["GET"])
@require_logged_in_user
def show_activity_to_edit(trip_id, activity_id):
    schedule = g.storage.get_itinerary(trip_id)
    trip = get_trip_heading(schedule, trip_id, g.storage)
    plans_by_date = {}

    for activity in schedule: 
        date = activity['at_date'] or ""
        if date not in plans_by_date:
            plans_by_date[date] = []

        plans_by_date[date].append(activity)
    return render_template("itinerary.html", plans_by_date=plans_by_date, trip=trip, edit_activity_id=activity_id)


@app.route("/trips/<int:trip_id>/activity/add", methods = ["POST"])
@require_logged_in_user
def add_new_plan(trip_id):
    date = request.form['date'] or None
    time = request.form['time'] or None
    activity = request.form['activity'].strip()
    note = request.form['note'].strip() or None
    cost = remove_punc_for_cost(request.form['cost']) or None

    error = error_for_activity_input(date, time, activity, cost)
    if error:
        flash(error, "error")
        return redirect(url_for('trip_schedule', 
                                trip_id=trip_id, 
                                time=time, 
                                activity=activity, 
                                note=note, 
                                cost=cost)
                                )

    g.storage.add_new_activity(date, time, activity, note, cost, trip_id)
    flash("Activity added.", "success")
    return redirect(url_for('trip_schedule', trip_id = trip_id))



@app.route("/trips/<int:trip_id>/activities/<int:activity_id>/edit", methods=["POST"])
@require_logged_in_user
def edit_activity(trip_id, activity_id):
    time = request.form['time'] or None
    activity = request.form['activity'].strip()
    note = request.form['note'].strip() or None
    cost = remove_punc_for_cost(request.form['cost']) or None

    error = error_for_activity_input('', time, activity, cost)
    if error:
        flash(error, "error")
        return redirect(url_for('edit_activity', trip_id = trip_id, activity_id=activity_id))

    g.storage.edit_activity_info(time, activity, note, cost, trip_id, activity_id)
    flash("Itinerary updated!", "success")
    return redirect(url_for('trip_schedule', trip_id=trip_id))


@app.route("/trips/<int:trip_id>/days/<day>/delete", methods=["POST"])
@require_logged_in_user
def delete_trip_day(trip_id, day):
    day = None if day == 'no_date' else day
    g.storage.delete_day_for_trip(trip_id, day)
    flash("Day deleted.", "success")
    return redirect(url_for('trip_schedule', trip_id=trip_id))


@app.route("/trips/<int:trip_id>/activiites/<int:activity_id>/delete", methods=["POST"])
@require_logged_in_user
def delete_activity(trip_id, activity_id):
    g.storage.delete_activity_by_id(trip_id, activity_id)
    flash("Activity deleted.", "success")
    return redirect(url_for('trip_schedule', trip_id = trip_id))


if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=5003)