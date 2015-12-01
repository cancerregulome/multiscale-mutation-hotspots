from app_logging import get_logger
log = get_logger()

from hotspots.database_util import sql_connection

PATHWAY_ASSOC_TABLE = 'pathway_assoc'


def get_pathway_data(tumor_type, gene, cluster):
    query_tpl = 'SELECT cancer as tumor_type, gene, cluster, pathway_name, pval, fdr, wl.url ' \
                'FROM {pathway_assoc_table} a ' \
                'LEFT OUTER JOIN pathway_web_links wl ON a.pathway_name=wl.pathway ' \
                'WHERE a.gene=? AND a.cancer=? AND a.cluster=? '
    query = query_tpl.format(pathway_assoc_table=PATHWAY_ASSOC_TABLE)

    log.debug("PATHWAY_ASSOC SQL: " + query)

    values = [gene, tumor_type, cluster]

    db = sql_connection()
    cursor = db.cursor()
    cursor.execute(query, tuple(values))

    items = []
    for row in cursor.fetchall():
        items.append(row)

    log.debug("Found {0} pathway associations.".format(len(items)))

    cursor.close()
    db.close()
    return items
