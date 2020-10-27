"""views - route function declarations and blueprint"""
import json

import flask
import whv

import telegraphist.message

blueprint = flask.Blueprint('webhooks', __name__)


@blueprint.route('/travis-ci<string:tld>', methods=['POST'])
def travisci_route(tld):
    """Handle webhook from Travis CI

    Because Travis uses a different public key for their .com and .org
    instances, we need to capture this from the URL.
    """
    # pylint: disable=protected-access
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

    telegraphist.message.send(
        'travis-ci.tmpl',
        build_url=payload['build_url'],
        build_number=payload['number'],
        repo_slug=repo_slug,
        build_state=payload['state']
    )

    return ''


@blueprint.route('/github')
def github_route():
    """Handle webook from GitHub"""
    return 'request went to /github'
