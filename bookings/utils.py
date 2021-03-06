from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Token authentication module for requests."""

    def __init__(self, token: str):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
