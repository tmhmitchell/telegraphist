"""message - sending telegram messages

Moved to its own module to avoid circular importing
"""
import flask
import requests

from telegraphist.config import TelegraphistConfig, KEY


def send_message(template_name, **message_data):
    config: TelegraphistConfig = flask.current_app.config[KEY]

    message_text = flask.render_template(template_name, **message_data)
    requests.post(
        url=f'https://api.telegram.org/bot{config.telegram.bot_token}/sendMessage',
        data={
            'chat_id': config.telegram.chat_id,
            'text': message_text,
            'parse_mode': 'html'
        }
    )
