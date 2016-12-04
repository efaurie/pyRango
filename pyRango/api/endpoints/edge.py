from pyRango.api.endpoints.meta import Endpoint


class EdgeEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/edge'

    def list(self, collection_id, start_vertex, direction='BOTH'):
        if direction.upper() not in ['BOTH', 'IN', 'OUT']:
            direction = 'BOTH'

        if direction.upper() == 'BOTH':
            return self._get(self.build_uri(collection_id), vertex=start_vertex)
        else:
            return self._get(self.build_uri(collection_id), direction=direction.lower())
