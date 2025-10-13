import psycopg2
from contextlib import contextmanager
from psycopg2.extras import DictCursor

class Database:
    
    @contextmanager
    def _database_connect(self):
        connection = psycopg2.connect(dbname='wanderly')
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def get_vacations(self):
        query = 'SELECT * FROM vacations'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                vacations = cursor.fetchall()
        return vacations
    
    def get_itinerary(self, vacation_id):
        query = 'SELECT * FROM plans WHERE vacation_id = %s'
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (vacation_id,))
                schedule = cursor.fetchall()
        return schedule
