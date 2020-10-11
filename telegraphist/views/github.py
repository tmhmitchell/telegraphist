import flask

bp = flask.Blueprint('github', __name__)


@bp.route('/github')
def webhook():
    return 'request went to /github'
