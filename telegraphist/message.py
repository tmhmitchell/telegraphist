"""message - sending telegram messages

Moved to its own module to avoid circular importing
"""
import flask
import requests

import telegraphist.config


def send(template_name, **message_data):
    """Send a message via the Telegram API

    The bot the message is send as and the chat ID it's sent to are set via
    the config file under the telegram settings.
    """
    config = flask.current_app.config[telegraphist.config.KEY]

    message_text = flask.render_template(template_name, **message_data)
    requests.post(
        url=f'https://api.telegram.org/bot{config.telegram.bot_token}/sendMessage',
        data={
            'chat_id': config.telegram.chat_id,
            'text': message_text,
            'parse_mode': 'html'
        }
    )
