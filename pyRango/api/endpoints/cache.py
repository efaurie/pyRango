from pyRango.api.endpoints.meta import Endpoint


class CacheEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/query-cache'

    def clear(self):
        self._delete(self.build_uri())

    def get_properties(self):
        self._get(self.build_uri('properties'))

    def set_properties(self, mode=None, max_results=None):
        parameters = dict()
        if mode:
            parameters['mode'] = mode
        if max_results:
            parameters['max_results'] = max_results
        self._put(self.build_uri('properties'), payload=parameters)
