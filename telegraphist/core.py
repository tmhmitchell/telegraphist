import flask
import gunicorn.app.base
import requests

import telegraphist.config
import telegraphist.views


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
        if options is None:
            self.options = {}
        else:
            self.options = options

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


def send_message(template_name, **message_data):
    message_text = flask.render_template(template_name, **message_data)

    chat_id = flask.current_app.config[telegraphist.config.TG_CHAT_ID]
    bot_token = flask.current_app.config[telegraphist.config.TG_BOT_TOKEN]

    requests.post(
        url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
        data={
            'chat_id': chat_id,
            'text': message_text,
            'parse_mode': 'html'
        }
    )


def create_wsgi_app():
    app = flask.Flask(
        import_name=__name__, template_folder='message-templates')
    app.config.update(telegraphist.config.get_config())

    app.register_blueprint(telegraphist.views.github.bp)
    app.register_blueprint(telegraphist.views.travisci.bp)
    return app


def run():
    wsgi = create_wsgi_app()
    Telegraphist(wsgi).run()
