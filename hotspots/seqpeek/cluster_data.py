from app_logging import get_logger
log = get_logger()

import re

from hotspots.database_util import sql_connection

CLUSTER_TABLE = 'clusters_tumor'
CLUSTER_MUTATION_FIELDS = ['missense_mutations', 'nonsense_mutations', 'silent_mutations']
# Breaks down the cluster string from the database:
# "100-200" -> ('100', '200')
CLUSTER_RE = re.compile('(\d+)-(\d+)')

def parse_cluster(row):
    start_str, end_str = CLUSTER_RE.findall(row['cluster'])[0]
    start = int(start_str)
    end = int(end_str)
    mutations_dict = {key: row[key] for key in CLUSTER_MUTATION_FIELDS}
    return {
        'tumor_type': row['tumor_type'],
        'start': start,
        'end': end,
        'mutation_stats': mutations_dict
    }

def get_cluster_data(tumor_type_array, gene):
    # Generate the 'IN' statement string: (%s, %s, ..., %s)
    tumor_stmt = ', '.join(['?' for tumor in tumor_type_array])

    query_tpl = 'SELECT cancer as tumor_type, gene, cluster, missense_mutations, nonsense_mutations, silent_mutations '\
                'FROM {cluster_table} '\
                'WHERE gene=? AND cancer IN ({tumor_stmt})'
    query = query_tpl.format(cluster_table=CLUSTER_TABLE, tumor_stmt=tumor_stmt)

    log.debug("CLUSTER SQL: " + query)

    values = [gene]
    values.extend(tumor_type_array)

    db = sql_connection()
    cursor = db.cursor()
    cursor.execute(query, tuple(values))

    items = []
    for row in cursor.fetchall():
        cluster = parse_cluster(row)
        items.append(cluster)

    cursor.close()
    db.close()
    return items
