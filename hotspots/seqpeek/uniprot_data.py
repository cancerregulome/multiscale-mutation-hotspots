import logging
_log = logging.getLogger("werkzeug")

from hotspots.database_util import sql_connection

UNIPROT_TABLE = 'uniprot'


def get_uniprot_data(uniprot_id):
    """

    :param uniprot_id:
    :return:
    """
    query_tpl = 'SELECT primary_accession, entry_name, length, protein_name ' \
                'FROM {uniprot_table} ' \
                'WHERE primary_accession=?'
    query = query_tpl.format(uniprot_table=UNIPROT_TABLE)

    _log.debug("UNIPROT SQL: " + query)

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
        return None

    return items[0]
