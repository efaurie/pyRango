from .meta import Writable


class Collection(Writable):
    def __init__(self, client, database, name):
        self.client = client
        self.database = database
        self.name = name

    def commit(self):
        pass