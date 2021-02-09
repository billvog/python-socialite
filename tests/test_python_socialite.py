import pytest
from unittest.mock import patch
from python_socialite import python_socialite
from python_socialite.python_socialite import OAuthProvider
from python_socialite.drivers.abstract_driver import AbstractDriver


config = {
    "google": {
        "client_id": "client_id_1",
        "client_secret": "***",
        "redirect_url": "http://localhost.com",
        "scopes": ["email", "user"],
    },
}


class TestDriver(AbstractDriver):
    __test__ = False

    def __init__(self, config):
        """Initialize test class."""
        super().__init__(config)
        self.scopes = config.get("scopes", ["openid", "email", "profile"])

    def get_auth_url(self):
        super().get_auth_url()

    def get_token_url(self):
        super().get_token_url()

    def get_user_by_token(self, access_token):
        super().get_user_by_token("")

    def map_user_to_dict(self, raw_user):
        super().map_user_to_dict(raw_user)

    def get_code_fields(self, state=None):
        fields = super().get_code_fields(state)
        return fields


@pytest.fixture
def token():
    token = {
        "access_token": "123",
        "id_token": "",
        "token_type": "Bearer",
        "scope": "profile",
    }

    return token


def test_python_socialite():
    if python_socialite is None:
        raise AssertionError


@patch("python_socialite.drivers.abstract_driver.requests")
def test_get_token(mock_requests, token):
    mock_requests.post.return_value.ok = True
    mock_requests.post.return_value.json.return_value = token
    code = "__testcode__"
    state = "one"
    provider = OAuthProvider("google", config)
    auth_token = provider.get_token(code, state)

    if auth_token.get("access_token") != "123":
        raise AssertionError

    if auth_token.get("token_type") != "Bearer":
        raise AssertionError


def test_set_scopes():
    with pytest.raises(ValueError):
        provider = OAuthProvider("invalid", config)
        provider.set_scopes(["error"])


def test_abstract_methods():
    driver = TestDriver(config)

    with pytest.raises(NotImplementedError):
        driver.get_auth_url()

    with pytest.raises(NotImplementedError):
        driver.get_token_url()

    with pytest.raises(NotImplementedError):
        driver.get_user_by_token("")

    with pytest.raises(NotImplementedError):
        driver.map_user_to_dict({})

    fields = driver.get_code_fields("sample")
    if fields.get("state") != "sample":
        raise AssertionError
