import flask
import gunicorn.app.base

from telegraphist import views


class Telegraphist(gunicorn.app.base.BaseApplication):
    """Wrap a flask application in Gunicorn.

    Adapted from:
    https://gitlab.tymlez.com/os/bigchaindb/-/blob/20d3dd4f/bigchaindb/web/server.py
    """

    def __init__(self, app, options=None):
        """Initialize a new standalone application.

        Args:
            app: A wsgi Python application.
            options (dict): the configuration.

        """
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        return {}
        # config = dict((key, value) for key, value in self.options.items()
        #               if key in self.cfg.settings and value is not None)

        # for key, value in config.items():
        #     # not sure if we need the `key.lower` here, will just keep
        #     # keep it for now.
        #     self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def create_wsgi_app():
    app = flask.Flask(__name__)
    app.register_blueprint(views.github.bp)
    app.register_blueprint(views.travisci.bp)
    return app


def run():
    wsgi = create_wsgi_app()
    Telegraphist(wsgi).run()
