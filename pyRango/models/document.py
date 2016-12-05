from .meta import Writable


class Document(Writable):
    def __init__(self, collection, handle=None, data=None):
        self.collection = collection
        self.http_client = self.collection.http_client
        self.handle = handle
        self.data = data

        if handle:
            self.populate(handle)

    def populate(self, handle):
        self.data = self.collection.http_client.document.get(handle)

    def commit(self):
        if self.handle:
            self.http_client.document.update(self.handle, self.data)
        else:
            self.http_client.document.create(self.collection.name, self.data)
