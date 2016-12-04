from pyRango.api.endpoints.meta import Endpoint


class QueryEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/query'

    @classmethod
    def filter_properties(cls, kwargs):
        for key in kwargs:
            if key not in ['slow_query_threshold', 'enabled', 'max_slow_queries',
                           'track_slow_queries', 'max_query_string_length']:
                kwargs.pop(key)
        return kwargs

    def parse(self, query):
        self._post(self.build_uri(), payload={'query': query})

    def get_properties(self):
        self._get(self.build_uri('properties'))

    def set_properties(self, **kwargs):
        self._put(self.build_uri('properties'), payload=self.filter_properties(kwargs))

    def get_running(self):
        self._get(self.build_uri('current'))

    def get_slow(self):
        self._get(self.build_uri('slow'))

    def kill(self, query_id):
        self._delete(self.build_uri(query_id))
