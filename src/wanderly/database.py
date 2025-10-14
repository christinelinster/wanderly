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

    def get_trips(self):
        query = 'SELECT * FROM trips'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
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
    

    def get_user_credentials(self, username):
        query = 'SELECT * FROM users WHERE username = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (username,))
                user = cursor.fetchone()
        return user 
