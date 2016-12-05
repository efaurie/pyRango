from .meta import Writable
from .document import Document


class Collection(Writable):
    def __init__(self, http_client, database, name, new=False):
        self.http_client = http_client
        self.database = database

        self.is_new = new
        self._cached_documents = list()

        self.info = {'name': name}
        self.properties = dict()

        if not new:
            self._populate()

    @property
    def name(self):
        return self.info['name']

    def _populate(self):
        self.info = self.http_client.collection.get(self.name)
        self.properties = self.http_client.collection.get_properties(self.name)

    def commit_documents(self):
        for document in self._cached_documents:
            document.commit()

    def commit(self):
        if self.is_new:
            self.http_client.collection.create(self.name, **self.properties)
        else:
            modifications = {}
            if 'wait_for_sync' in self.properties:
                modifications['wait_for_sync'] = self.properties['wait_for_sync']
            if 'journal_size' in self.properties:
                modifications['journal_size'] = self.properties['journal_size']
            self.http_client.collection.set_properties(self.name, **modifications)

        self.commit_documents()

    def create_document(self, data):
        document = Document(self, data=data)
        self._cached_documents.append(document)
        return document

    def get_document(self, handle):
        document = Document(self, handle=handle)
        return document
