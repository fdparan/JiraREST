import requests
from requests.auth import HTTPBasicAuth


class Server:
    def __init__(self, base_url, user=None, password=None, use_latest=False):
        self.context = "/rest/api/latest" if use_latest else "/rest/api/2"

        self.base = base_url
        self._uri()

        self.auth_token = requests.auth.HTTPBasicAuth(user, password) if user and password else None

    def _uri(self):
        self.uri = self.base + self.context

    def change_base_url(self, new_base_url):
        self.base = new_base_url
        self._uri()

    def get_operation(self, resource, verbose=False):
        return requests.get(self._rest_call(resource, verbose), auth=self.auth_token).json()

    def _rest_call(self, resource, verbose=False):
        call = self.uri + resource
        if verbose:
            print(call)
        return call

    def get_projects(self):
        return self.get_operation("/project")
