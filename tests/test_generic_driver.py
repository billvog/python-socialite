import requests
from python_socialite.drivers.abstract_driver import AbstractDriver
from python_socialite.drivers.abstract_user import abstract_user
from python_socialite.python_socialite import OAuthProvider


config = {
    "generic": {
        "client_id": "client_id_1",
        "client_secret": "***",
        "redirect_url": "http://localhost.com",
        "scopes": ["email", "user"],
    },
}


class GenericProvider(AbstractDriver):
    def __init__(self, config):
        """Initialize Google provider."""
        super().__init__(config)
        self.scopes = config.get("scopes", ["account", "email"])

    @staticmethod
    def provider_name():
        return "generic"

    def get_auth_url(self, state=None):
        url = "https://example.com/site/oauth2/authorize"
        return self.build_url(url, state)

    def get_token_url(self):
        return "https://example.com/site/oauth2/access_token"

    def get_user_by_token(self, access_token):
        return {}

    def map_user_to_dict(self, raw_user):
        user = dict(abstract_user)
        user["id"] = raw_user.get("account_id", "1")
        return user


def test_generic_methods():
    provider = OAuthProvider(GenericProvider, config)
    state = "one"
    auth_url = provider.get_auth_url(state)

    if not auth_url.find("example.com"):
        raise AssertionError
