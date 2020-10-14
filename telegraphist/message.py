"""message - sending telegram messages

Moved to its own module to avoid circular importing
"""
import flask

import telegraphist.config


def send_message(template_name, **message_data):
    config: telegraphist.config.TelegraphistConfig = flask.current_app.config[
        telegraphist.config.KEY]

    config.github

    message_text = flask.render_template(template_name, **message_data)

    requests.post(
        url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
        data={
            'chat_id': '',
            'text': message_text,
            'parse_mode': 'html'
        }
    )
