"""core - run a Telegraphist instance"""

import flask
import gunicorn.app.base
import gunicorn.app.wsgiapp
import gunicorn.config

import telegraphist.config
import telegraphist.views


class TelegraphistApplication(gunicorn.app.base.Application):
    """Wrap a flask application in Gunicorn.

    Adapted from:
    https://gitlab.tymlez.com/os/bigchaindb/-/blob/20d3dd4f/bigchaindb/web/server.py
    """

    # pylint: disable=super-init-not-called
    def __init__(self, app):
        """Initialize a new standalone application.

        Args:
            app: A wsgi Python application.
            options (dict): the configuration.
        """
        self.callable = app
        self.logger = None
        self.cfg = gunicorn.config.Config(
            usage='',
            prog='telegraphist'
        )
        self.load_config()

    def load_config(self):
        # Return access logs to the stdout
        self.cfg.settings['accesslog'].value = '-'

    def init(self, *_):
        """Do nothing - I'm not even sure what init does"""

    def load(self):
        """Do nothing - we set callable in __init__"""


def create_wsgi_app():
    """Configures a Flask instance that can be run by a wSGI server"""
    app = flask.Flask(
        import_name=__name__, template_folder='message-templates')
    app.config[telegraphist.config.KEY] = telegraphist.config.get_config()

    app.register_blueprint(telegraphist.views.blueprint)
    return app


def run():
    """Let's gooooooooooooooo!"""
    wsgi = create_wsgi_app()
    TelegraphistApplication(wsgi).run()
