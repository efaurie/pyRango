from pyRango.api.endpoints.meta import Endpoint


class DatabaseEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/database'

    def build_uri(self, *args):
        return '{BASE}/{ARGS}'.format(BASE=self.endpoint_uri, ARGS='/'.join(args))

    def current(self):
        return self.get(self.build_uri('current'))
