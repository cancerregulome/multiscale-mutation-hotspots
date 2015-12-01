from sqlite3 import connect, Row
from django.conf import settings

def sql_connection():
    # TODO FIX this should be configurable, not hardcoded
    conn = connect('mica.sqlite3')
    conn.row_factory = Row

    return conn

