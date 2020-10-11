import json

import flask
import whv

import telegraphist.core

bp = flask.Blueprint('travis-ci', __name__)


@bp.route('/travis-ci<string:tld>', methods=['POST'])
def webhook(tld):
    if tld not in (whv.travisci._TLD_ORG, whv.travisci._TLD_COM):
        return ''

    serialised_payload = flask.request.form['payload']

    try:
        valid = whv.travisci.verify(
            payload=serialised_payload.encode(),
            signature=flask.request.headers['Signature'].encode(),
            tld=tld
        )
    except KeyError:
        return '', 401

    if not valid:
        return '', 401

    payload = json.loads(serialised_payload)

    repo_owner = payload['repository']['owner_name']
    repo_name = payload['repository']['name']
    repo_slug = f'{repo_owner}/{repo_name}'

    telegraphist.core.send_message(
        'travis-ci.tmpl',
        build_url=payload['build_url'],
        build_number=payload['number'],
        repo_slug=repo_slug,
        build_state=payload['state']
    )

    return ''
