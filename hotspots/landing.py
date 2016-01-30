from flask import render_template

from app_logging import get_logger
log = get_logger()

from hotspots.seqpeek.view import format_tumor_type_list
from hotspots.seqpeek.tumor_types import tumor_types as ALL_TUMOR_TYPES

try:
    from hotspots.seqpeek.gene_list import gene_list as GENE_LIST
except ImportError:
    log.error("Loading gene list failed, using static list.")
    GENE_LIST = ['EGFR', 'TP53', 'PTEN']


TEMPLATE_NAME = 'hotspots/landing.html'


def landing_page_view():
    tumor_types_for_tpl = format_tumor_type_list(ALL_TUMOR_TYPES)

    template_args = {
        'static_data': {
            'gene_list': GENE_LIST,
        },
        'gene_select_widget': {
            'action': '/seqpeek',
            'tumor_type_select': False,
            'all_tumor_types': tumor_types_for_tpl,
            'include_summary_paramater': True,
            'button_label': 'Find mutations'
        },
    }

    return render_template(TEMPLATE_NAME, **template_args)

