from pyRango.api.endpoints.meta import Endpoint


class TraversalEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/traversal'