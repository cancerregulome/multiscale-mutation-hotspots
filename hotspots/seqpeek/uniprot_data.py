import logging

from hotspots.database_util import sql_connection

UNIPROT_TABLE = 'uniprot'

class UniProtEntryNotFound(Exception):
    def __init__(self, uniprot_id):
        self.message = uniprot_id

def get_uniprot_data(uniprot_id):
    query_tpl = 'SELECT primary_accession, entry_name, length, protein_name ' \
                'FROM {uniprot_table} ' \
                'WHERE primary_accession=?'
    query = query_tpl.format(uniprot_table=UNIPROT_TABLE)

    logging.debug("UNIPROT SQL: " + query)

    values = [uniprot_id]

    db = sql_connection()
    cursor = db.cursor()
    cursor.execute(query, tuple(values))

    items = []
    for row in cursor.fetchall():
        res = {k: row[k] for k in row.keys()}
        items.append(res)

    cursor.close()
    db.close()

    if len(items) == 0:
        raise UniProtEntryNotFound(uniprot_id)

    return items[0]
