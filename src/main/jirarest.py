import requests
from requests.auth import HTTPBasicAuth


class Server:
    def __init__(self, base_url, user=None, password=None, use_latest=False):
        self.context = "/rest/api/latest" if use_latest else "/rest/api/2"

        self.base = base_url
        self.auth_token = requests.auth.HTTPBasicAuth(user, password) if user and password else None

    def uri(self):
        return self.base + self.context

    def change_base_url(self, new_base_url):
        self.base = new_base_url

    def get_operation(self, resource, verbose=False):
        return requests.get(self.generate_rest(resource, verbose), auth=self.auth_token).json()

    def generate_rest(self, resource, verbose=False):
        rest_uri = self.uri() + resource
        if verbose:
            print(rest_uri)
        return rest_uri

    def get_projects(self, get_keys=None):

        projects = self.get_operation("/project")

        if get_keys:
            projects = list(map(lambda x: dict((k, x[k] if k in x.keys() else None) for k in get_keys), projects))

        return projects
