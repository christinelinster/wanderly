# ✨ Wanderly ✨

Wanderly is a Flask-based travel itinerary planner that helps users organize trips, activities, notes, costs, and more in one seamless web application. They can create multi-day travel plans, log activities by date and time, manage costs, and view all trip details through a clean and responsive interface.

---

## Features

- **Trip Management**: Create, view, edit, and delete trips.
- **Itinerary Planner**: Add metadata for activities, ordered by date and time.
- **Cost Tracking**: Record and view estimated costs for each activity or day.
- **User Authentication**: Secure login and session management.
- **Pagination**: Browse trips and itineraries efficiently with paginated views.
- **Form Validation**: Ensure consistent input formats with client and server-side validation for dates, times, and costs.
- **Responsive Front-End**: HTML, CSS, and Javscript-based UI that adapts to different devices so you can plan at the desk or on the go.

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Python 3.13.7 (Flask) |
| Frontend | HTML, CSS, JavaScript |
| Database | PostgreSQL 17.6 |
| Database Adapter | psycopg2 |
| Templates | Jinja2 |
| Dependency Management | Poetry |

---

## Prerequisites

Before starting Wanderly, ensure you have the following:
- **Python** 3.13.7
- **PostgreSQL** 17.6
- **Poetry** for dependency management
- Tested on **Google Chrome Version 141**

## Getting Started
1. Navigate to the correct directory
```bash
cd wanderly
```

2. Install Dependencies
```bash
poetry install
```
This creates a virtual environment and installs all required packages listed in `pyproject.toml`.

3. Set Up PostgreSQL Database
```bash
psql postgres
CREATE DATABASE wanderly;
\q
```

4. Run the Application
```bash
cd src/wanderly
poetry run python app.py
```

Visit http://localhost:5003 in your browser.


## Future Improvements

- View previous trips and itineraries
- Automatically calculate total cost by day and trip
- Interactive map to locate activites for each day
- Filter and sort activities based on tags (e.g., food, activity, location)
- Collaborative trip planning
- Notification system for upcoming activities
- Email / SMS reminders for scheduled tasks
