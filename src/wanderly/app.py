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
    error_for_page,
    plans_by_date,
    plans_per_page,
    total_pages,
    remove_punc_for_cost,
)

import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
TRIPS_PER_PAGE = 8
DAYS_PER_PAGE = 4

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


def require_trip(f):
    @wraps(f)
    @require_logged_in_user
    def decorated_function(*args, **kwargs):
        trip_id = kwargs.get('trip_id')
        trip = g.storage.find_trip_by_id(trip_id)
        if not trip:
            flash('Trip not found.', 'error')
            return redirect(url_for('index'))
        return f(trip, *args, **kwargs)
    return decorated_function


def require_activity(f):
    @wraps(f)
    @require_trip
    def decorated_function(trip, *args, **kwargs):
        activity_id = kwargs.get('activity_id')
        activity = g.storage.find_activity_by_id(activity_id)
        if not activity:
            flash('Activity not found.', 'error')
            return redirect(url_for('show_trip_schedule', trip_id=trip['id']))
        return f(activity, trip, *args, **kwargs)
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

    if not g.storage.user_exists(email):
        flash("The email is not in our records.", "error")
        return render_template('login.html')

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

    flash("Invalid credentials.", "error")
    return render_template("login.html")

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
    page = request.args.get('page', 1, type=int)
    total_items = g.storage.get_trip_count(session['user_id'])
    pages = total_pages(total_items, TRIPS_PER_PAGE)
    
    error = error_for_page(page, pages)
    if error:
        flash(error['message'], 'error')
        return redirect(url_for('show_trips', page=error['page']))

    offset = (page - 1) * TRIPS_PER_PAGE

    trips = g.storage.get_trips_by_user_id(session['user_id'], limit=TRIPS_PER_PAGE, offset=offset)
    first_name = get_first_name(trips, session['user_id'], g.storage)

    return render_template("trips.html", 
                           first_name=first_name, 
                           trips=trips, 
                           current_page=page, 
                           pages=pages
                           )


# Create require activity decorator 
@app.route("/trips/<int:trip_id>/edit", methods=["GET"])
@require_trip
def show_trip_to_edit(trip, trip_id):
    page = request.args.get('page', 1, type=int)
    total_items = g.storage.get_trip_count(session['user_id'])
    pages = total_pages(total_items, TRIPS_PER_PAGE)

    error = error_for_page(page, pages)
    if error:
        flash(error['message'], 'error')
        return redirect(url_for('show_trip_to_edit', trip_id=trip_id, page=error['page']))

    offset = (page - 1) * TRIPS_PER_PAGE

    trips = g.storage.get_trips_by_user_id(session['user_id'], limit=TRIPS_PER_PAGE, offset=offset)
    first_name = get_first_name(trips, session['user_id'], g.storage)

    return render_template("trips.html", 
                           first_name=first_name, 
                           trips=trips, 
                           edit_trip_id=trip_id, 
                           current_page=page, 
                           pages=pages
                           )


@app.route("/trips/<int:trip_id>/edit", methods=["POST"])
@require_trip
def edit_trip(trip, trip_id):
    destination = request.form['destination'].strip()
    start_date = request.form['start_date'] or None
    end_date = request.form['end_date'] or None
    page = request.form.get('page', 1, type=int)

    error = error_for_trips(destination, start_date, end_date)
    if error:
        flash(error, "error")
        return redirect(url_for('show_trip_to_edit', trip_id=trip_id, page=page))

    g.storage.edit_trip_heading(destination, start_date, end_date, trip_id)
    flash("Trip saved.", "success")
    return redirect(url_for('show_trips', page=page))


@app.route("/trips/<int:trip_id>", methods=['POST'])
@require_trip
def delete_trip(trip, trip_id):
    page = request.form.get('page', 1, type=int)
    g.storage.delete_trip_by_id(trip_id)
    flash("Trip deleted.", "success")
    return redirect(url_for('show_trips',page=page))


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
    total_items = g.storage.get_trip_count(session['user_id'])
    page = total_pages(total_items, TRIPS_PER_PAGE)

    flash('Your new adventure has been created!', "success")
    return redirect(url_for('show_trips', page=page))


# ---- ITINERARY ----
@app.route("/trips/<int:trip_id>")
@require_trip
def show_trip_schedule(trip, trip_id):
    all_plans = g.storage.get_itinerary(trip_id)
    itinerary = plans_by_date(all_plans)

    page = request.args.get('page', 1, type=int)
    pages = total_pages(len(itinerary.keys()), DAYS_PER_PAGE)
    error = error_for_page(page, pages)
    if error:
        flash(error['message'], 'error')
        return redirect(url_for('show_trip_schedule', trip_id=trip_id, page=error['page']))
    
    plans = plans_per_page(itinerary, page, DAYS_PER_PAGE)

    time = request.args.get("time", "")
    activity = request.args.get("activity", "")
    note = request.args.get("note", "")
    cost = request.args.get("cost", "")

    return render_template("itinerary.html", 
                           plans=plans, 
                           trip=trip,
                           time=time,
                           activity=activity,
                           note=note,
                           cost=cost,
                           current_page = page,
                           pages=pages
                           )


@app.route("/trips/<int:trip_id>/activities/<int:activity_id>/edit", methods=["GET"])
@require_activity
def show_activity_to_edit(activity, trip, trip_id, activity_id):
    all_plans = g.storage.get_itinerary(trip_id)
    itinerary = plans_by_date(all_plans)

    page = request.args.get('page', 1, type=int)
    pages = total_pages(len(itinerary.keys()), DAYS_PER_PAGE)
    error = error_for_page(page, pages)
    if error:
        flash(error['message'], 'error')
        return redirect(url_for('show_trip_schedule', trip_id=trip_id, page=error['page']))
    
    plans = plans_per_page(itinerary, page, DAYS_PER_PAGE)

    return render_template("itinerary.html", 
                           plans=plans, 
                           trip=trip, 
                           edit_activity_id=activity_id,
                           current_page=page,
                           pages=pages
                           )


@app.route("/trips/<int:trip_id>/activity/add", methods = ["POST"])
@require_trip
def add_new_plan(trip_id):
    page = request.form.get('page', 1, type=int)
    date = request.form['date'] or None
    time = request.form['time'] or None
    activity = request.form['activity'].strip()
    note = request.form['note'].strip() or None
    cost = remove_punc_for_cost(request.form['cost']) or None

    error = error_for_activity_input(date, time, activity, cost)
    if error:
        flash(error, "error")
        return redirect(url_for('show_trip_schedule', 
                                trip_id=trip_id, 
                                time=time, 
                                activity=activity, 
                                note=note, 
                                cost=cost)
                                )

    g.storage.add_new_activity(date, time, activity, note, cost, trip_id)
    flash("Activity added.", "success")
    return redirect(url_for('show_trip_schedule', trip_id = trip_id, page=page))


@app.route("/trips/<int:trip_id>/activities/<int:activity_id>/edit", methods=["POST"])
@require_activity
def edit_activity(activity, trip, trip_id, activity_id):
    page = request.form.get('page', 1, type=int)
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
    return redirect(url_for('show_trip_schedule', trip_id=trip_id, page=page))


@app.route("/trips/<int:trip_id>/days/<day>/delete", methods=["POST"])
@require_trip
def delete_trip_day(trip_id, day):
    page = request.form.get('page', 1, type=int)
    day = None if day == 'no-date' else day
    g.storage.delete_day_for_trip(trip_id, day)
    flash("Day deleted.", "success")
    return redirect(url_for('show_trip_schedule', trip_id=trip_id, page=page))


@app.route("/trips/<int:trip_id>/activiites/<int:activity_id>/delete", methods=["POST"])
@require_activity
def delete_activity(activity, trip, trip_id, activity_id):
    page = request.form.get('page', 1, type=int)
    g.storage.delete_activity_by_id(trip_id, activity_id)
    flash("Activity deleted.", "success")
    return redirect(url_for('show_trip_schedule', trip_id = trip_id, page=page))


if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=5003)