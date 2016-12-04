from pyRango.api.endpoints.meta import Endpoint, ArangoError


class DocumentEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/document'

    def get(self, handle):
        return self._get(self.build_uri(handle))

    def get_header(self, handle):
        return self._head(self.build_uri(handle))

    def create(self, collection_name, data):
        return self._post(self.build_uri(collection_name), payload=data, transform=False)

    def replace(self, handle, data):
        return self._put(self.build_uri(handle), payload=data, transform=False)

    def replace_many(self, collection, data):
        return self._put(self.build_uri(collection), payload=data, transform=False)

    def update(self, handle, data):
        return self._patch(self.build_uri(handle), payload=data, transform=False)

    def update_many(self, collection, data):
        return self._patch(self.build_uri(collection), payload=data, transform=False)

    def delete(self, handle):
        return self._delete(self.build_uri(handle))

    def delete_many(self, collection, data):
        return self._delete(self.build_uri(collection), payload=data, transform=False)
