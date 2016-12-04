from pyRango.api.endpoints.meta import Endpoint


class ExplainEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/explain'

    def create(self, query):
        self._post(self.build_uri(), payload={'query': query})
