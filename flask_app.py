from flask import Flask, request, render_template

from app_logging import get_logger
from hotspots.seqpeek.view import seqpeek as seqpeek_view

log = get_logger()

app = Flask(__name__)


@app.route('/')
def landing_page():
    return(render_template("hotspots/landing.html"))


@app.route('/seqpeek/',  defaults={'gene': '', 'tumor': ''})
def seqpeek(gene, tumor):
    request_gene = request.args.get('gene')
    request_tumor_list = [str(t) for t in request.args.getlist('tumor')]
    return(seqpeek_view(request_gene, request_tumor_list))

if __name__ == '__main__':
    app.run(debug=True)
