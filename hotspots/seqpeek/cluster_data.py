from MySQLdb import connect
from MySQLdb.cursors import DictCursor
import logging
from os import getenv
import re

from django.conf import settings

CLUSTER_TABLE = 'clusters'
CLUSTER_MUTATION_FIELDS = ['missense_mutations', 'nonsense_mutations', 'silent_mutations']
# Breaks down the cluster string from the database:
# "100-200" -> ('100', '200')
CLUSTER_RE = re.compile('(\d+)-(\d+)')

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

def parse_cluster(row):
    start_str, end_str = CLUSTER_RE.findall(row['cluster'])[0]
    start = int(start_str)
    end = int(end_str)
    mutations_dict = {key: row[key] for key in CLUSTER_MUTATION_FIELDS}
    return {
        'start': start,
        'end': end,
        'mutation_stats': mutations_dict
    }

def get_cluster_data(tumor_type_array, gene):
    # Generate the 'IN' statement string: (%s, %s, ..., %s)
    tumor_stmt = ', '.join(['%s' for tumor in tumor_type_array])

    query_tpl = 'SELECT cancer, gene, cluster, missense_mutations, nonsense_mutations, silent_mutations '\
                'FROM {cluster_table} '\
                'WHERE gene=%s AND cancer IN ({tumor_stmt})'
    query = query_tpl.format(cluster_table=CLUSTER_TABLE, tumor_stmt=tumor_stmt)

    logging.debug("CLUSTER SQL: " + query)

    values = [gene]
    values.extend(tumor_type_array)

    db = sql_connection()
    cursor = db.cursor(DictCursor)
    cursor.execute(query, tuple(values))

    items = []
    for row in cursor.fetchall():
        cluster = parse_cluster(row)
        items.append(cluster)

    cursor.close()
    db.close()
    return items
