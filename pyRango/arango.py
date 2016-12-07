from pyRango.api import ArangoHttpClient
from pyRango.models import Collection
from pyRango.models import Graph


class ArangoClient(object):
    def __init__(self, host='localhost', port=8529, database='_system', username=None, password=None, cert=None):
        self.api_parameters = {
            'host': host,
            'port': port,
            'database': database,
            'username': username,
            'password': password,
            'cert': cert
        }
        self.http_client = ArangoHttpClient(**self.api_parameters)

    @property
    def database(self):
        return self.api_parameters['database']

    def change_database(self, new_database):
        self.api_parameters['database'] = new_database
        self.http_client = ArangoHttpClient(**self.api_parameters)

    def create_collection(self, name):
        return Collection(self.http_client, self.database, name, new=True)

    def get_collection(self, name):
        return Collection(self.http_client, self.database, name)

    def create_graph(self, name):
        return Graph(self.http_client, self.database, name, new=True)

    def get_graph(self, name):
        return Graph(self.http_client, self.database, name)
