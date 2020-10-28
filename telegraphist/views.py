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
    repo_slug = flask.request.headers['Travis-Repo-Slug']

    build_state_translations = {
        'Pending': 'is pending',
        'Passed': 'has passed',
        'Fixed': 'was fixed',
        'Broken': 'has broken',
        'Failed': 'has failed',
        'Still Failing': 'has failed again',
        'Canceled': 'was cancelled',
        'Errored': 'has errored'
    }

    telegraphist.message.send(
        'travis-ci.tmpl',
        build_url=payload['build_url'],
        build_number=payload['number'],
        repo_slug=repo_slug,
        build_state=build_state_translations[payload['status_message']]
    )

    return ''


@blueprint.route('/github', methods=['POST'])
def github_route():
    """Handle webook from GitHub"""
    return 'request went to /github'
