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
        query = 'SELECT * FROM plans WHERE trip_id = %s ORDER BY activity_date, activity_time'
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
    
    def find_id_by_username(self, username):
        query = 'SELECT id from users WHERE username = %s'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                user_id = cursor.fetchone()
        return user_id[0]

    def get_user_credentials(self, email):
        query = 'SELECT * FROM users WHERE email = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (email,))
                user = cursor.fetchone()
        return user 

    def create_new_trip(self, destination, start_date, end_date, user_id ):
        query = 'INSERT INTO trips (destination, depart_date, return_date, user_id) VALUES(%s, %s, %s, %s)'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (destination, start_date, end_date, user_id,))
    
    def delete_trip_by_id(self, trip_id):
        query = 'DELETE FROM trips WHERE id = %s'
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (trip_id, ))
