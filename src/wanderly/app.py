from flask import (
    Flask,
    flash,
    g,
    render_template,
    redirect
)

import secrets
from database import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.before_request
def load_db():
    g.storage = Database()

@app.route("/")
def index():
    vacations = g.storage.get_vacations()
    return render_template("home.html", vacations=vacations)

@app.route('/<vacation_id>')
def vacation_schedule(vacation_id):
    schedule = g.storage.get_itinerary(vacation_id)
    return render_template("itinerary.html", schedule=schedule)

if __name__ == "__main__":
    app.run(debug=True, port=5003)