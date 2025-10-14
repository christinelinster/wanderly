from flask import (
    Flask,
    flash,
    g,
    render_template,
    redirect
)

from filters import safe_default
import secrets
from database import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

app.jinja_env.filters['safe_default'] = safe_default

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
    schedule = g.storage.get_schedule(trip_id)
    plans_by_date = {}

    for activity in schedule: 
        date = activity['activity_date']

        if date not in plans_by_date:
            plans_by_date[date] = []

        plans_by_date[date].append(activity)

    return render_template("itinerary.html", schedule=plans_by_date, trip=trip)


if __name__ == "__main__":
    app.run(debug=True, port=5003)