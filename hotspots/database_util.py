from sqlite3 import connect, Row
from django.conf import settings

def sql_connection():
    # Connecting to localhost
    database = settings.DATABASES['default']
    conn = connect(database['NAME'])
    conn.row_factory = Row

    return conn

