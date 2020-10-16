"""config - application configuration"""

import os

import dataclasses
import yaml


TELEGRAPHIST_CONFIG_PATH = 'TELEGRAPHIST_CONFIG_PATH'
KEY = 'TELEGRAPHIST_CONFIG'


@dataclasses.dataclass
class Repos:
    """A namspace for repo settings"""
    _repos: dict

    def __init__(self, config):
        self._repos = config

    def get_secret(self, slug):
        """Retrieve the webhook secret for a given repository"""
        try:
            return self._repos[slug]
        except KeyError as exc:
            text = 'Repo {slug} isn\'t in configuration file - no way to verify'
            raise KeyError(text) from exc


@dataclasses.dataclass
class GitHub:
    """Namespace for GitHub repo settings"""
    repos: Repos

    def __init__(self, config):
        self.repos = Repos(config['repos'])


@dataclasses.dataclass
class Telegram:
    """Namespace for Telegram settings.

    For us to communicate with Telegram, we need to know
    1. Which bot account as we "speaking as"
    2. Which chat are we sending messages to?
    """
    bot_token: str
    chat_id: str

    def __init__(self, config):
        self.bot_token = config['bot-token']
        self.chat_id = config['chat-id']


@dataclasses.dataclass
class TelegraphistConfig:
    """Container class for application config.

    Allows items to be access in a namspaced, autosuggestion-friendly manner.
    """
    telegram: Telegram
    github: GitHub

    def __init__(self, config):
        self.telegram = Telegram(config['telegram'])
        self.github = GitHub(config['github'])


def get_config():
    """Create a configuration object from the environment

    Returns:
        TelegraphistConfig: an instance populated with data read from the
            specified config file
    """
    try:
        config_path = os.environ[TELEGRAPHIST_CONFIG_PATH]

        with open(config_path) as file_descriptor:
            config_as_dict = yaml.load(file_descriptor, Loader=yaml.SafeLoader)
            return TelegraphistConfig(config_as_dict)

    except KeyError as exc:
        text = f'Could not find environment variable {exc.args[0]}'
        raise KeyError(text) from exc

    except yaml.parser.ParserError as exc:
        text = 'Could not parse config file. Are you sure it\'s valid YAML?'
        raise ValueError(text) from exc
