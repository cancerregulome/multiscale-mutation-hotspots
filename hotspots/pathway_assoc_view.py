from flask import render_template

from hotspots.seqpeek.pathway_assoc_data import get_pathway_data
from hotspots.seqpeek.view import sanitize_gene_input, sanitize_normalize_tumor_type

TEMPLATE_NAME = 'hotspots/pathway_assoc.html'


def sort_pathways(pathways):
    result = sorted(pathways, key='pval')
    return result

def pathway_assoc_view(request_gene, request_tumor_type, request_cluster):
    template_args = {}

    pathway_data = get_pathway_data(request_tumor_type, request_gene, request_cluster)
    sorted_pathways = sorted(pathway_data, key=lambda row: row['pval'])

    template_args = {
        'pathways': sorted_pathways
    }

    return render_template(TEMPLATE_NAME, **template_args)
