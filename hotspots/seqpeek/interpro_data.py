from app_logging import get_logger
log = get_logger()

from hotspots.database_util import sql_connection

INTERPRO_TABLE = 'interpro_domains'

class InterProEntryNotFound(Exception):
    def __init__(self, uniprot_id):
        self.message = uniprot_id

def get_protein_domain_data(uniprot_id):
    query_tpl = 'SELECT interpro_id, name, database, start, end ' \
                'FROM {interpro_table} ' \
                'WHERE uniprot_accession=?'
    query = query_tpl.format(interpro_table=INTERPRO_TABLE)

    log.debug("INTERPRO SQL: " + query)

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
        raise InterProEntryNotFound(uniprot_id)

    return items
