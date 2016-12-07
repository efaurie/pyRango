from .meta import Writable


class Document(Writable):
    def __init__(self, collection, id_=None, key_=None, rev_=None, data=None):
        self.collection = collection
        self.http_client = self.collection.http_client
        self.id_ = id_
        self.key_ = key_
        self.rev_ = rev_
        self.data = data

        if self.id_:
            self.populate()

    def populate(self):
        self.data = self.http_client.document.get(self.id_)

    def commit(self):
        if self.id_:
            self.http_client.document.update(self.id_, self.data)
        else:
            response = self.http_client.document.create(self.collection.name, self.data)
            self.id_ = response['_id']
            self.key_ = response['_key']
            self.rev_ = response['_rev']
