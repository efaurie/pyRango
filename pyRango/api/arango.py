import logging

import requests

from pyRango.api.endpoints import DatabaseEndpoint

LOG = logging.getLogger(__name__)


class ArangoClient(object):
    def __init__(self, host='localhost', port=8529, database='_system', username=None, password=None, cert=None):
        self.host = host
        self.port = port
        self.basic_auth = (username, password)
        self.cert = cert
        self._database = database

        self.session = requests.Session()
        self._authenticate()

        self.database = DatabaseEndpoint(self)

    def set_database(self, new_database):
        self._database = new_database

    @property
    def base_uri(self):
        return 'http://{HOSTNAME}:{PORT}'.format(HOSTNAME=self.host, PORT=str(self.port))

    @property
    def admin_uri(self):
        return '{BASE}/_admin'.format(BASE=self.base_uri)

    @property
    def db_uri(self):
        if self._database:
            return '{BASE}/_db/{DATABASE}'.format(BASE=self.base_uri, DATABASE=self._database)
        else:
            return '{BASE}/_db'.format(BASE=self.base_uri)

    def _authenticate(self):
        if self.cert:
            self.session.cert = self.cert

        if self.basic_auth[0] and self.basic_auth[1]:
            self.session.auth = self.basic_auth
