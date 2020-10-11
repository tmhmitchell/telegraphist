import os

TG_BOT_TOKEN = 'TG_BOT_TOKEN'
TG_CHAT_ID = 'TG_CHAT_ID'


def get_config():
    try:
        return {
            TG_BOT_TOKEN: os.environ[TG_BOT_TOKEN],
            TG_CHAT_ID: os.environ[TG_CHAT_ID],
        }
    except KeyError as exc:
        text = f'Could not find environment variable {exc.args[0]}'
        raise KeyError(text) from exc
