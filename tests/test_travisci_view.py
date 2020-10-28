import pytest
import sentry_sdk
import whv

import telegraphist.config
import telegraphist.core
import telegraphist.message


@pytest.fixture
def client(monkeypatch):
    def mock_init(*_, **__):
        return

    def mock_verify(*_, **__):
        return True

    # Configure telegraphist instance with a mock config file
    monkeypatch.setenv(
        telegraphist.config.TELEGRAPHIST_CONFIG_PATH, 'tests/data/test-config.yml')

    # Don't initialise sentry
    monkeypatch.setattr(sentry_sdk, 'init', mock_init)

    # Don't bother verifying hooks for our tests
    monkeypatch.setattr(whv.travisci, 'verify', mock_verify)

    return telegraphist.core.create_wsgi_app().test_client()


def _make_mock_send(expected_build_state):
    def mock_send(_, **message_data):
        assert message_data == {
            'build_number': '8288',
            'build_state': expected_build_state,
            'build_url': 'https://travis-ci.com/travis-ci/docs-travis-ci-com/builds/193615133',
            'repo_slug': 'travis-ci/docs-travis-ci-com'
        }

    return mock_send


def test_passing_hook(client, monkeypatch):
    # Patch out hook verification and message-sending
    monkeypatch.setattr(
        telegraphist.message, 'send', _make_mock_send('has passed'))

    # Grab Travis' example payload to send
    with open('tests/data/travis-ci/webhook-passed.json') as descriptor:
        payload = descriptor.read()

    response = client.post(
        path='/travis-ci.org',
        data={'payload': payload},
        headers={
            'Signature': 'blahblahblahblah',
            'Travis-Repo-Slug': 'travis-ci/docs-travis-ci-com'
        }

    )
    assert response.status_code == 200


def test_failed(client, monkeypatch):
    # Patch out hook verification and message-sending
    monkeypatch.setattr(
        telegraphist.message, 'send', _make_mock_send('has failed'))

    # Grab Travis' example payload to send
    with open('tests/data/travis-ci/webhook-failed.json') as descriptor:
        payload = descriptor.read()

    response = client.post(
        path='/travis-ci.org',
        data={'payload': payload},
        headers={
            'Signature': 'blahblahblahblah',
            'Travis-Repo-Slug': 'travis-ci/docs-travis-ci-com'
        }

    )
    assert response.status_code == 200
