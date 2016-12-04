from pyRango.api.endpoints.meta import Endpoint


class CursorEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/cursor'

    def create(self, query):
        self._post(self.build_uri(), payload={'query': query})

    def next(self, cursor_id):
        self._put(self.build_uri(cursor_id))

    def delete(self, cursor_id):
        self._delete(self.build_uri(cursor_id))
