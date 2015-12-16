from flask import Flask, request, render_template
from jinja2 import FileSystemLoader
import os

from app_logging import get_logger
from hotspots.seqpeek.view import seqpeek as seqpeek_view
from hotspots.pathway_assoc_view import pathway_assoc_view

log = get_logger()

app = Flask(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

@app.route('/')
def landing_page():
    return(render_template("hotspots/landing.html"))


@app.route('/seqpeek/',  defaults={'gene': '', 'tumor': ''})
def seqpeek(gene, tumor):
    request_gene = request.args.get('gene')
    request_tumor_list = [str(t) for t in request.args.getlist('tumor')]
    return(seqpeek_view(request_gene, request_tumor_list))


@app.route('/pathway/', defaults={'gene': '', 'tumor': '', 'cluster': ''})
def pathway_assoc(gene, tumor, cluster):
    request_gene = request.args.get('gene')
    request_tumor = request.args.get('tumor')
    request_cluster = request.args.get('cluster')
    log.debug("{0} {1} {2}".format(request_gene, request_tumor, request_cluster))
    return(pathway_assoc_view(request_gene, request_tumor, request_cluster))


if __name__ == '__main__':
    app.run(debug=True)
    app.jinja_loader = FileSystemLoader(TEMPLATE_DIR)
