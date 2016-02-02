from flask import Flask, abort, request, render_template
from jinja2 import FileSystemLoader
import os

from app_logging import get_logger
from hotspots.landing import landing_page_view
from hotspots.seqpeek.view import seqpeek as seqpeek_view
from hotspots.pathway_assoc_view import pathway_assoc_view

log = get_logger()

app = Flask(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

@app.errorhandler(500)
def error_500(error):
    return render_template('hotspots/error.html')

@app.route('/')
def landing_page():
    try:
        return landing_page_view()
    except Exception as e:
        log.exception(e)
        abort(500)


@app.route('/seqpeek/',  defaults={'gene': '', 'tumor': '', 'summary': ''})
def seqpeek(gene, tumor, summary):
    try:
        request_gene = request.args.get('gene')
        request_tumor_list = [str(t) for t in request.args.getlist('tumor')]
        summary = False
        if request.args.get('summary') == 'true':
            summary = True

        return seqpeek_view(request_gene, request_tumor_list, summary_only=summary)
    except Exception as e:
        log.exception(e)
        abort(500)


@app.route('/pathway/', defaults={'gene': '', 'tumor': '', 'cluster': ''})
def pathway_assoc(gene, tumor, cluster):
    try:
        request_gene = request.args.get('gene')
        request_tumor = request.args.get('tumor')
        request_cluster = request.args.get('cluster')
        log.debug("{0} {1} {2}".format(request_gene, request_tumor, request_cluster))
        return pathway_assoc_view(request_gene, request_tumor, request_cluster)
    except Exception as e:
        log.exception(e)
        abort(500)


if __name__ == '__main__':
    app.run(debug=True)
    app.jinja_loader = FileSystemLoader(TEMPLATE_DIR)
