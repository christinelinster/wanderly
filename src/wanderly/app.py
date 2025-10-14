from flask import (
    Flask,
    flash,
    g,
    render_template,
    redirect
)

from filters import (
    safe_default, 
    formatted_date,
    formatted_title_date,
    formatted_time
    )

import secrets
from database import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

app.jinja_env.filters['safe_default'] = safe_default
app.jinja_env.filters['formatted_date'] = formatted_date
app.jinja_env.filters['formatted_title_date'] = formatted_title_date
app.jinja_env.filters['formatted_time'] = formatted_time

@app.before_request
def load_db():
    g.storage = Database()

@app.route("/")
def index():
    trips = g.storage.get_trips()
    return render_template("home.html", trips=trips)

@app.route("/trips/<int:trip_id>")
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

@app.route("/trips/new")
def plan_new_trip():
    return render_template("create_trip.html")

if __name__ == "__main__":
    app.run(debug=True, port=5003)