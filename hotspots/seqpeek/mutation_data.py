from MySQLdb.cursors import DictCursor
import logging

from hotspots.database_util import sql_connection

MUTATION_TABLE = 'mutations'

def parse_cluster(row):
    return {
        'tumor_type': row['tumor_type'],
        'gene': row['gene'],
        'patient_barcode': row['patient_id'],
        'mutation_type': row['mutation_type'],
        'amino_acid_position': row['aa_location'],
        'dna_change': row['aa_change'],
        'amino_acid_mutation': row['aa1'],
        'amino_acid_wildtype': row['aa2']
    }

def get_mutation_data(tumor_type_array, gene):
    # Generate the 'IN' statement string: (%s, %s, ..., %s)
    tumor_stmt = ', '.join(['%s' for tumor in tumor_type_array])

    query_tpl = 'SELECT Cancer AS tumor_type, gene, tumor_sample AS patient_id, mutation_type, aa_change, aa_location, aa1, aa2 ' \
                'FROM {mutation_table} ' \
                'WHERE gene=%s AND Cancer IN ({tumor_stmt})'
    query = query_tpl.format(mutation_table=MUTATION_TABLE, tumor_stmt=tumor_stmt)

    logging.debug("MUTATION SQL: " + query)

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
