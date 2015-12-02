from flask import render_template

from hotspots.seqpeek.pathway_assoc_data import get_pathway_data
from hotspots.seqpeek.view import sanitize_normalize_tumor_type

from app_logging import get_logger
log = get_logger()

try:
    from hotspots.seqpeek.gene_list import gene_list as GENE_LIST
except ImportError:
    log.error("Loading gene list failed, using static list.")
    GENE_LIST = ['EGFR', 'TP53', 'PTEN']


TEMPLATE_NAME = 'hotspots/pathway_assoc.html'


def sanitize_gene_input(gene_param):
    gene_set = frozenset(GENE_LIST)
    if gene_param in gene_set:
        return gene_param
    else:
        log.error("{0} - Unknown gene '{1}'".format(__name__, gene_param))
        return None


def pathway_assoc_view(request_gene, request_tumor_type, request_cluster):
    template_args = {
        'data_found': False
    }

    gene = sanitize_gene_input(request_gene)
    tumor_list = sanitize_normalize_tumor_type([request_tumor_type])

    if gene is None or len(tumor_list) == 0:
        return render_template(TEMPLATE_NAME, **template_args)

    tumor_type = tumor_list[0]
    pathway_data = get_pathway_data(tumor_type, gene, request_cluster)
    sorted_pathways = sorted(pathway_data, key=lambda row: row['pval'])

    if len(pathway_data) == 0:
        return render_template(TEMPLATE_NAME, **template_args)

    template_args.update({
        'gene_label': gene,
        'tumor_type': tumor_type,
        'pathways': sorted_pathways,
        'data_found': True
    })

    return render_template(TEMPLATE_NAME, **template_args)
