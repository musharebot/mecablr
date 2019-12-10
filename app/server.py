# -*- coding: utf-8 -*-
"""Flask Application
"""
import json
from os import path
from flask import Flask, abort, request, Response, render_template
from flask_bootstrap import Bootstrap
from main import mecab_utils

CONFIG_PATH = path.join(path.dirname(path.abspath(__file__)), 'flask.cfg')
DIC_DIR = path.join('/', 'usr', 'local', 'lib', 'mecab', 'dic')

# Flask Application
app = Flask(__name__)
app.config.from_pyfile(CONFIG_PATH)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    name = None
    form = TextForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/analysis', methods=['GET'])
def parse():
    """Morphological Analysis by MeCab.

    Request Format:
        GET: /?sentence=アルミ缶の上にあるみかん
    """
    # STEP.1 Extraction of a given sentence
    sentence = ""
    try:
        sentence = request.args['sentence']
    except KeyError:
        abort(400, '`sentence` not found.')
    # STEP.2 Morphological Analysis
    result = None
    if sentence is not None:
        # sentence = normalize(sentence)
        result = mecab_utils.parse_sentence(sentence, nbest_num=1)

    # STEP.3 Make a response object
    payload = json.dumps(result, ensure_ascii=False)
    res = {
        'response': payload,
        'status': 200,
        'content_type': 'application/json'
    }
    return Response(**res)
