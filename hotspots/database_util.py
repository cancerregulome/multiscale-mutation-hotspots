from os import getenv
from MySQLdb import connect
from django.conf import settings

def sql_connection():
    server_env = getenv('SERVER_SOFTWARE')
    if server_env and server_env.startswith('Google App Engine/'):
        database = settings.DATABASES['default']
        conn = connect(
            unix_socket=database['HOST'],
            db=database['NAME'],
            user=database['USER'],
        )
    else:
        # Connecting to localhost
        database = settings.DATABASES['data']
        conn = connect(
            host='127.0.0.1',
            port=3306,
            db=database['NAME'],
            user=database['USER'],
            passwd=database['PASSWORD']
        )

    return conn

