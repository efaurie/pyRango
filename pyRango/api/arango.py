import logging

import requests

from pyRango.api.endpoints import EdgeEndpoint
from pyRango.api.endpoints import GraphEndpoint
from pyRango.api.endpoints import DocumentEndpoint
from pyRango.api.endpoints import DatabaseEndpoint
from pyRango.api.endpoints import TraversalEndpoint
from pyRango.api.endpoints import CollectionEndpoint

LOG = logging.getLogger(__name__)


class ArangoClient(object):
    def __init__(self, host='localhost', port=8529, database='_system', username=None, password=None, cert=None):
        self.host = host
        self.port = port
        self.basic_auth = (username, password)
        self.cert = cert
        self.current_database = database

        self.session = requests.Session()
        self._authenticate()

        self.edge = EdgeEndpoint(self)
        self.graph = GraphEndpoint(self)
        self.traversal = TraversalEndpoint(self)
        self.database = DatabaseEndpoint(self)
        self.collection = CollectionEndpoint(self)
        self.document = DocumentEndpoint(self)

    @property
    def base_uri(self):
        return 'http://{HOSTNAME}:{PORT}'.format(HOSTNAME=self.host, PORT=str(self.port))

    @property
    def admin_uri(self):
        return '{BASE}/_admin'.format(BASE=self.base_uri)

    @property
    def db_uri(self):
        if self.current_database:
            return '{BASE}/_db/{DATABASE}'.format(BASE=self.base_uri, DATABASE=self.current_database)
        else:
            return '{BASE}/_db'.format(BASE=self.base_uri)

    @property
    def api_uri(self):
        return '{BASE}/_api'.format(BASE=self.base_uri)

    def _authenticate(self):
        if self.cert:
            self.session.cert = self.cert

        if self.basic_auth[0] and self.basic_auth[1]:
            self.session.auth = self.basic_auth
