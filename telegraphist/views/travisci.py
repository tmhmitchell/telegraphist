import flask
import whv

bp = flask.Blueprint('travis-ci', __name__)


@bp.route('/travis-ci/<string:tld>', methods=['POST'])
def webhook(tld):
    tld_org = whv.travisci._TLD_ORG[1:]
    tld_com = whv.travisci._TLD_COM[1:]

    if tld not in (tld_org, tld_com):
        return ''

    try:
        valid = whv.travisci.verify(
            flask.request.form['payload'].encode(),
            flask.request.headers['Signature'].encode(),
            '.' + tld
        )
    except KeyError:
        return '', 401

    if not valid:
        return '', 401

    return f'request went to /travis-ci{tld}'
