from contextlib import contextmanager
import os
import psycopg2
from psycopg2.extras import DictCursor


class Database:

    @contextmanager
    def _database_connect(self):
        if os.environ.get('FLASK_ENV') =='production':
            connection = psycopg2.connect(os.environ['DATABASE_URL'])
        else:
            connection = psycopg2.connect(dbname='wanderly')

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def __init__(self):
        self._setup_schema()

    def _setup_schema(self):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM information_schema.tables
                               WHERE table_schema = 'public' AND table_name = 'users'
                               """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                                   CREATE TABLE users(
                                        id SERIAL PRIMARY KEY,
                                        full_name varchar(255) NOT NULL,
                                        email varchar(255) UNIQUE NOT NULL,
                                        password text NOT NULL,
                                        created_at date NOT NULL DEFAULT now()
                                    );
                                   """)
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM information_schema.tables
                               WHERE table_schema = 'public' AND table_name = 'trips'
                               """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                                   CREATE TABLE trips(
                                        id serial PRIMARY KEY,
                                        destination text NOT NULL,
                                        depart_date date,
                                        return_date date,
                                        user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE
                                    );
                                   """)
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM information_schema.tables
                               WHERE table_schema = 'public' AND table_name = 'plans'
                               """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                                   CREATE TABLE plans(
                                        id serial PRIMARY KEY,
                                        at_date date,
                                        at_time time,
                                        activity text NOT NULL,
                                        cost numeric CHECK (cost >= 0.00),
                                        note text,
                                        trip_id integer NOT NULL,
                                        FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
                                    );
                                    """)

# -------- AUTH --------
    def user_exists(self, email):
        return self.get_user_credentials(email)

    def create_new_user(self, name, email, password):
        query = """
                INSERT INTO users (full_name, email, password)
                VALUES (%s, %s, %s)
                """
        values = (name, email, password,)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

    def get_user_credentials(self, email):
        query = 'SELECT * FROM users WHERE email ILIKE %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (email,))
                user = cursor.fetchone()
        return user


# -------- TRIPS --------
    def get_trip_count(self, user_id):
        query = 'SELECT COUNT(*) FROM trips where user_id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id,))
                row =  cursor.fetchone()
        return row['count']

    def get_name_by_id(self, user_id):
        query = 'SELECT full_name from users WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
        return row['full_name']

    def get_trips_by_user_id(self, user_id, limit, offset):
        query = """
                SELECT users.full_name AS name, trips.*
                FROM trips
                JOIN users ON trips.user_id = users.id
                WHERE trips.user_id = %s
                ORDER BY trips.depart_date, trips.return_date, trips.id
                LIMIT %s OFFSET %s
                """

        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id, limit, offset,))
                trips = cursor.fetchall()
        return trips

    def edit_trip_heading(self, destination, start_date, end_date, trip_id):
        query = """
                UPDATE trips
                SET destination = %s,
                depart_date = %s,
                return_date = %s
                WHERE id = %s
                """

        values = (destination, start_date, end_date, trip_id,)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

    def create_new_trip(self, destination, start_date, end_date, user_id ):
        query = """
                INSERT INTO trips (destination, depart_date, return_date, user_id)
                VALUES (%s, %s, %s, %s)
                """
        values = (destination, start_date, end_date, user_id,)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

    def delete_trip_by_id(self, trip_id):
        query = 'DELETE FROM trips WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (trip_id, ))

    def find_trip_by_id(self, trip_id):
        query = 'SELECT * FROM trips WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (trip_id,))
                trip = cursor.fetchone()
        return trip

# -------- ITINERARY --------
    def get_itinerary(self, trip_id):
        query = """
                SELECT *
                FROM plans
                WHERE plans.trip_id = %s
                ORDER BY at_date, at_time, plans.id
                """
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (trip_id,))
                itinerary = cursor.fetchall()
        return itinerary

    def is_healthy(self):
        """A lightweight check that the database can be reached.

        Returns True when a simple query succeeds, False otherwise.
        This is used by health/readiness endpoints to determine if the
        application is ready to receive traffic.
        """
        try:
            with self._database_connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT 1')
                    cursor.fetchone()
            return True
        except Exception:
            return False

    def add_new_activity(self, date, time, title, note, cost, trip_id):
        query = """
                INSERT INTO plans (at_date, at_time, activity, note, cost, trip_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        values = (date, time, title, note, cost, trip_id,)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

    def delete_day_for_trip(self, trip_id, day):
        query = 'DELETE FROM plans WHERE trip_id = %s and at_date = %s'
        values = (trip_id, day,)

        if not day:
            query = 'DELETE FROM plans WHERE trip_id = %s and at_date IS NULL'
            values = (trip_id,)

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

    def delete_activity_by_id(self, trip_id, activity_id):
        query = 'DELETE FROM plans WHERE trip_id = %s AND id = %s'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (trip_id, activity_id,))

    def edit_activity_info(
            self,
            date,
            time,
            title,
            note,
            cost,
            trip_id,
            activity_id
            ):
        query = """
                UPDATE plans
                SET at_date = %s,
                at_time = %s,
                activity = %s,
                note = %s,
                cost = %s
                WHERE trip_id = %s AND id = %s
                """
        values = (date, time, title, note, cost, trip_id, activity_id, )
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

    def find_activity_by_id(self, activity_id):
        query = 'SELECT * FROM plans WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (activity_id,))
                activity = cursor.fetchone()
        return activity
