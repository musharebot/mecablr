# -*- coding: utf-8 -*-
"""Flask Application
"""
import json
from os import path
from flask import Flask, abort, request, Response
import MeCab


CONFIG_PATH = path.join(path.dirname(path.abspath(__file__)), 'flask.cfg')
DIC_DIR = path.join('/', 'usr', 'local', 'lib', 'mecab', 'dic')


# Flask Application
app = Flask(__name__)
app.config.from_pyfile(CONFIG_PATH)

# MeCab
mecab = MeCab.Tagger()


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
        parsed = mecab.parse(sentence)
        result = []
        for line in parsed.split('\n'):
            line = line.strip()
            elems = line.split('\t', 1)
            if line == 'EOS' or len(elems) <= 1:
                continue
            cols = ['Surface', 'PoS', 'PoS1', 'PoS2', 'PoS3',
                    'VerbConjugation', 'Original', 'Reading', 'Pronunciation']
            result.append(dict(zip(cols, [elems[0]] + elems[1].split(','))))
    # STEP.3 Make a response object
    payload = json.dumps({'sentence': sentence, 'result': result}, ensure_ascii=False)
    res = {
        'response': payload,
        'status': 200,
        'content_type': 'application/json'
    }
    return Response(**res)
