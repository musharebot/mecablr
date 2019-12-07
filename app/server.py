# -*- coding: utf-8 -*-
"""Flask Application
"""
import json
from os import path
from flask import Flask, abort, request, Response
from main import mecab_utils

CONFIG_PATH = path.join(path.dirname(path.abspath(__file__)), 'flask.cfg')
DIC_DIR = path.join('/', 'usr', 'local', 'lib', 'mecab', 'dic')


# Flask Application
app = Flask(__name__)
app.config.from_pyfile(CONFIG_PATH)


@app.route('/', methods=['GET'])
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
