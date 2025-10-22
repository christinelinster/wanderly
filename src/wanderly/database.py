import psycopg2
from contextlib import contextmanager
from psycopg2.extras import DictCursor
from itertools import groupby
from operator import itemgetter

class Database:
    
    @contextmanager
    def _database_connect(self):
        connection = psycopg2.connect(dbname='wanderly')
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def get_trips_by_user(self, user_id):
        query = 'SELECT users.full_name AS name, trips.* FROM trips JOIN users ON trips.user_id = users.id WHERE trips.user_id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id,))
                trips = cursor.fetchall()
        return trips
    
    def get_itinerary(self, trip_id):
        query = 'SELECT * FROM plans WHERE trip_id = %s ORDER BY at_date, at_time'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (trip_id,))
                itinerary = cursor.fetchall()

        return itinerary
    
    def find_trip_by_id(self, trip_id):
        query = 'SELECT * FROM trips WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (trip_id,))
                trip = cursor.fetchone()
        return trip
    
    def get_name_by_id(self, user_id):
        query = 'SELECT full_name from users WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id,))
                name = cursor.fetchone()
        return name

    def get_user_credentials(self, email):
        query = 'SELECT * FROM users WHERE email ILIKE %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (email,))
                user = cursor.fetchone()
        return user 
    
    def user_exists(self, email):
        return True if self.get_user_credentials(email) else False

    def create_new_user(self, name, email, password):
        query = 'INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, email, password,))

    def create_new_trip(self, destination, start_date, end_date, user_id ):
        query = 'INSERT INTO trips (destination, depart_date, return_date, user_id) VALUES(%s, %s, %s, %s)'
        values = (destination, start_date, end_date, user_id,)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
    
    def add_new_activity(self, date, time, title, note, cost, trip_id):
        query = 'INSERT INTO plans(at_date, at_time, activity, note, cost, trip_id) VALUES(%s, %s, %s, %s, %s, %s)'
        values = (date, time, title, note, cost, trip_id,)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

# Fix this 
    def delete_day_for_trip(self, trip_id, day):
        if not day:
            query = 'DELETE FROM plans WHERE trip_id = %s and at_date IS NULL'
            values = (trip_id,)
        else: 
            query = 'DELETE FROM plans WHERE trip_id = %s and at_date = %s'
            values = (trip_id, day,)

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)    

    def delete_trip_by_id(self, trip_id):
        query = 'DELETE FROM trips WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (trip_id, ))

    def delete_activity_by_id(self, trip_id, activity_id):
        query = 'DELETE FROM plans WHERE trip_id = %s AND id = %s'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (trip_id, activity_id,))

    def edit_trip_heading(self, destination, start_date, end_date, trip_id):
        query = 'UPDATE trips SET destination = %s, depart_date = %s, return_date = %s WHERE id = %s'
        values = (destination, start_date, end_date, trip_id,)
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)

    def edit_activity_info(self, time, title, note, cost, trip_id, activity_id):
        query = 'UPDATE plans SET at_time = %s, activity=%s, note=%s, cost=%s WHERE trip_id = %s AND id = %s'
        values = (time, title, note, cost, trip_id, activity_id, )
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
