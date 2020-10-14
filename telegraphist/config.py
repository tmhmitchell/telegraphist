"""config - application configuration"""

import os

import dataclassy
import yaml


TG_BOT_TOKEN = 'TG_BOT_TOKEN'
TG_CHAT_ID = 'TG_CHAT_ID'
TELEGRAPHIST_CONFIG_PATH = 'TELEGRAPHIST_CONFIG_PATH'
KEY = 'TELEGRAPHIST_CONFIG'


@dataclassy.dataclass(kwargs=True)
class Telegram:  # pylint: disable=too-few-public-methods
    """Namespace for Telegram settings.

    For us to communicate with Telegram, we need to know
    1. Which bot account as we "speaking as"
    2. Which chat are we sending messages to?
    """
    token: str
    chat_id: str


@dataclassy.dataclass(kwargs=True)
class Repos:  # pylint: disable=too-few-public-methods
    """Namespace for GitHub repo settings"""

    _repos: dict

    def get_secret(self, slug):
        """Retrieve the webhook secret for a given repository"""
        try:
            return self._repos[slug]
        except KeyError as exc:
            text = 'Repo {slug} isn\'t in configuration file - no way to verify'
            raise KeyError(text) from exc


@dataclassy.dataclass(kwargs=True)
class GitHub:  # pylint: disable=too-few-public-methods
    """Namespace for GitHub settings"""
    repos: Repos


@dataclassy.dataclass(kwargs=True)
class TelegraphistConfig:  # pylint: disable=too-few-public-methods
    """Container class for application config.

    Allows items to be access in a namspaced, autosuggestion-friendly manner.
    """
    telegram: Telegram
    github: GitHub


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
            return TelegraphistConfig(**config_as_dict)

    except KeyError as exc:
        text = f'Could not find environment variable {exc.args[0]}'
        raise KeyError(text) from exc

    except yaml.parser.ParserError as exc:
        text = 'Could not parse config file. Are you sure it\'s valid YAML?'
        raise ValueError(text) from exc
