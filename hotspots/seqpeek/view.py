from copy import deepcopy
import json
import logging
import re
from django.shortcuts import render
from mock_data import EGFR_GBM_LGG as FAKE_PLOT_DATA
from maf_api_mock_data import EGFR_BLCA_BRCA as FAKE_MAF_DATA
from hotspots.seqpeek.tumor_types import tumor_types as ALL_TUMOR_TYPES

logging.info("Loading gene list...")
try:
    from hotspots.seqpeek.gene_list import gene_list as GENE_LIST
except ImportError:
    logging.error("Loading gene list failed, using static list.")
    GENE_LIST = ['EGFR', 'TP53', 'PTEN']

from hotspots.seqpeek.uniprot_data import get_uniprot_data
from hotspots.seqpeek.interpro_data import get_protein_domain_data
from hotspots.seqpeek.cluster_data import get_cluster_data as get_cluster_data_remote
from hotspots.seqpeek.mutation_data import get_mutation_data as get_mutation_data_remote

SEQPEEK_VIEW_DEBUG_MODE = False
SEQPEEK_VIEW_MUTATION_DEBUG = False

SAMPLE_ID_FIELD_NAME = 'patient_barcode'
TUMOR_TYPE_FIELD = "tumor"
COORDINATE_FIELD_NAME = 'amino_acid_position'

MUTATION_DATA_PROTEIN_FIELD = 'uniprot_id'

PROTEIN_DOMAIN_DB = 'PFAM'

ALPHA_FINDER = re.compile('[\W_]+', re.UNICODE)

TEMPLATE_NAME = 'hotspots/seqpeek/view.html'

def get_number_of_unique_samples(track):
    # todo: change this to get total_rows from bigquery endpoint
    # note: result from this function isn't the same as total_rows from bigquery
    sample_ids = set()
    for mutation in track['mutations']:
        sample_ids.add(mutation[SAMPLE_ID_FIELD_NAME])

    return len(sample_ids)


# TODO remove if not needed
def clean_track_mutations(mutations_array):
    retval = []
    for mutation in mutations_array:
        cleaned = deepcopy(mutation)
        cleaned[COORDINATE_FIELD_NAME] = int(mutation[COORDINATE_FIELD_NAME])
        retval.append(cleaned)

    return retval


def sort_track_mutations(mutations_array):
    return sorted(mutations_array, key=lambda k: k[COORDINATE_FIELD_NAME])


def get_track_statistics(track):
    return {
        'samples': {
            'numberOf': get_number_of_unique_samples(track)
        }
    }


def filter_protein_domains(match_array):
    return [m for m in match_array if m['dbname'] == PROTEIN_DOMAIN_DB]


def get_table_row_id(tumor_type):
    return "seqpeek_row_{0}".format(tumor_type)


def build_seqpeek_regions(protein_data):
    return [{
        'type': 'exon',
        'start': 0,
        'end': protein_data['length']
    }]


def build_summary_track(tracks):
    all = []
    for track in tracks:
        all.extend(track["mutations"])

    return {
        'mutations': all,
        'label': 'COMBINED',
        'tumor': 'none-combined',
        'type': 'summary'
    }


def get_track_label(track):
    return track[TUMOR_TYPE_FIELD]


def get_protein_domains_local_debug(uniprot_id):
    return deepcopy(FAKE_PLOT_DATA['protein'])


def process_raw_domain_data(data):
    result = []
    for item in data:
        database = item['database']

        # Filter for PFAM
        if not database.startswith('PF'):
            continue

        domain = {
            'name': item['name'],
            'locations': [{
                'start': item['start'],
                'end': item['end']
            }],
            'dbname': 'PFAM',
            'ipr': {
                'type': 'Domain',
                'id': item['interpro_id'],
                'name': item['name']
            },
            'id': database
        }

        result.append(domain)

    logging.debug("Found {total} domains, filtered down to {num}".format(total=len(data), num=len(result)))
    return result

def get_protein_domains_remote(uniprot_id):
    uniprot_data = get_uniprot_data(uniprot_id)
    logging.debug("UniProt entry: " + str(uniprot_data))

    # Add protein domain data to the UniProt entry
    raw_domain_data = get_protein_domain_data(uniprot_id)
    domains = process_raw_domain_data(raw_domain_data)
    uniprot_data['matches'] = domains
    return uniprot_data


def get_protein_domains(uniprot_id):
    if SEQPEEK_VIEW_DEBUG_MODE:
        return get_protein_domains_local_debug(uniprot_id)
    else:
        return get_protein_domains_remote(uniprot_id)


def get_maf_data_debug(gene, tumor_type_list):
    return deepcopy(FAKE_PLOT_DATA['tracks'])


def get_maf_data_remote(gene, tumor_type_list):
    if SEQPEEK_VIEW_MUTATION_DEBUG:
        return get_maf_data_debug(gene, tumor_type_list)
    else:
        return get_mutation_data_remote(tumor_type_list, gene)


def get_mutation_data(gene, tumor_type_list):
    if SEQPEEK_VIEW_MUTATION_DEBUG:
        return deepcopy(FAKE_MAF_DATA['items'])
    else:
        return get_mutation_data_remote(tumor_type_list, gene)

def process_cluster_data_for_tumor(all_clusters, tumor_type):
    clusters = filter(lambda c: c['tumor_type'] == tumor_type, all_clusters)
    result = []
    for index, cluster in enumerate(clusters):
        item = {
            'name': '',
            'type': 'cluster',
            'id': 'cluster_' + str(index),
            'locations': [{
                'start': cluster['start'],
                'end': cluster['end']
            }],
            'mutation_stats': cluster['mutation_stats']
        }
        result.append(item)
    return result

def build_track_data(tumor_type_list, all_tumor_mutations, all_clusters):
    tracks = []
    for tumor_type in tumor_type_list:
        tracks.append({
            TUMOR_TYPE_FIELD: tumor_type,
            'mutations': filter(lambda m: m['tumor_type'] == tumor_type, all_tumor_mutations),
            'clusters': process_cluster_data_for_tumor(all_clusters, tumor_type)
        })

    return tracks

def find_uniprot_id(mutations):
    uniprot_id = None
    for m in mutations:
        if MUTATION_DATA_PROTEIN_FIELD in m:
            uniprot_id = m[MUTATION_DATA_PROTEIN_FIELD]
            break

    return uniprot_id

def get_cluster_data(tumor_type_array, gene):
    clusters = get_cluster_data_remote(tumor_type_array, gene)
    return clusters

def sanitize_gene_input(param_string):
    return ALPHA_FINDER.sub('', param_string)

def sanitize_normalize_tumor_type(tumor_type_list):
    tumor_set = frozenset(ALL_TUMOR_TYPES)
    sanitized = []
    for tumor_param in tumor_type_list:
        if tumor_param in tumor_set:
            sanitized.append(tumor_param)

    return sanitized

def seqpeek(request):
    context = {}

    if (('tumor' not in request.GET) or (request.GET['tumor'] == '')) or \
            (('gene' not in request.GET) or (request.GET['gene'] == '')):
        return render(request, TEMPLATE_NAME, context)

    # Remove non-alphanumeric characters from parameters and uppercase all
    gene = sanitize_gene_input(request.GET['gene']).upper()
    parsed_tumor_list = sanitize_normalize_tumor_type(request.GET.getlist('tumor'))
    logging.debug("Valid tumors from request: {0}".format(str(parsed_tumor_list)))

    if len(parsed_tumor_list) == 0:
        return render(request, TEMPLATE_NAME, context)

    cluster_data = get_cluster_data(parsed_tumor_list, gene)

    maf_data = get_mutation_data(gene, parsed_tumor_list)
    uniprot_id = find_uniprot_id(maf_data)
    logging.debug("Found UniProt ID: " + repr(uniprot_id))

    protein_data = get_protein_domains(uniprot_id)
    track_data = build_track_data(parsed_tumor_list, maf_data, cluster_data)

    plot_data = {
        'gene_label': gene,
        'tracks': track_data,
        'protein': protein_data
    }

    # Pre-processing
    # - Sort mutations by chromosomal coordinate
    for track in plot_data['tracks']:
        track['mutations'] = sort_track_mutations(track['mutations'])

    # Annotations
    # - Add label, possibly human readable
    # - Add type that indicates whether the track is driven by data from search or
    #   if the track is aggregate
    for track in plot_data['tracks']:
        track['type'] = 'tumor'
        track['label'] = get_track_label(track)

    plot_data['tracks'].append(build_summary_track(plot_data['tracks']))

    for track in plot_data['tracks']:
        # Calculate statistics
        track['statistics'] = get_track_statistics(track)
        # Unique ID for each row
        track['render_info'] = {
            'row_id': get_table_row_id(track[TUMOR_TYPE_FIELD])
        }

    plot_data['regions'] = build_seqpeek_regions(plot_data['protein'])
    plot_data['protein']['matches'] = filter_protein_domains(plot_data['protein']['matches'])
    plot_data['gene_list'] = GENE_LIST

    tumor_list = ','.join(parsed_tumor_list)

    context.update({
        'search': {},
        'plot_data': plot_data,
        'data_bundle': json.dumps(plot_data),
        'gene': gene,
        'tumor_list': tumor_list,
        'all_tumor_types': ALL_TUMOR_TYPES
    })

    return render(request, TEMPLATE_NAME, context)

