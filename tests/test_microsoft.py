import pytest
from urllib import parse
from unittest.mock import patch
from python_socialite.python_socialite import OAuthProvider
from python_socialite.exceptions import BadVerification

config = {
    "microsoft": {
        "client_id": "client_id_1",
        "client_secret": "***",
        "redirect_url": "http://localhost.com",
        "scopes": ["email", "user"],
        "tenant": "common",
    },
}


@pytest.fixture
def token():
    token = {
        "access_token": "access_token_1",
        "id_token": "",
        "token_type": "Bearer",
        "scope": "profile",
    }

    return token


def test_get_auth_url():
    provider = OAuthProvider("microsoft", config)
    state = "one"
    auth_url = provider.set_scopes(["email", "openid"]).get_auth_url(state)
    parts = list(parse.urlparse(auth_url))
    query = dict(parse.parse_qsl(parts[4]))

    if query.get("client_id") != "client_id_1":
        raise AssertionError


@patch("python_socialite.drivers.microsoft.requests")
def test_get_user(mock_requests):
    mock_requests.get.return_value.ok = True
    mock_requests.get.return_value.json.return_value = {
        "id": "xb56ksf",
        "name": "John Doe",
        "userPrincipalName": "john@example.com",
    }
    provider = OAuthProvider("microsoft", config)
    user = provider.get_user("xxxxxx")

    if user.get("provider") != "microsoft":
        raise AssertionError

    if user.get("id") != "xb56ksf":
        raise AssertionError

    if user.get("email") != "john@example.com":
        raise AssertionError

@patch("python_socialite.drivers.github.requests")
def test_get_token_error(mock_requests):
    mock_requests.get.return_value.ok = True
    mock_requests.get.return_value.json.return_value = {
        "error": "Bad verification code"
    }
    provider = OAuthProvider("microsoft", config)
    state = "one"

    with pytest.raises(BadVerification):
        provider.get_token("xxxxxx", state, type="form-data")
