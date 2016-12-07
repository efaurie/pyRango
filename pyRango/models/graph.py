from .meta import Writable
from .document import Document
from .collection import Collection


class Vertex(Document):
    def __init__(self, collection, id_=None, key_=None, rev_=None, data=None):
        super().__init__(collection, id_=id_, key_=key_, rev_=rev_, data=data)
        self.collection_name = collection.name
        self.graph_name = collection.graph_name

    def populate(self):
        self.data = self.http_client.graph.get_vertex(self.graph_name, self.collection_name, self.id_)

    def commit(self):
        if self.id_:
            self.http_client.graph.replace_vertex(self.graph_name, self.collection_name, self.id_, self.data)
        else:
            result = self.http_client.graph.create_vertex(self.graph_name, self.collection_name, self.data)
            self.id_ = result['vertex']['_id']
            self.key_ = result['vertex']['_key']
            self.rev_ = result['vertex']['_rev']


class Edge(Document):
    def __init__(self, collection, from_, to_, id_=None, key_=None, rev_=None, data=None):
        super().__init__(collection, id_=id_, key_=key_, rev_=rev_, data=data)
        self.collection_name = collection.name
        self.graph_name = collection.graph_name

        self.from_ = from_
        self.to_ = to_

    def populate(self):
        self.data = self.http_client.graph.get_edge(self.graph_name, self.collection_name, self.id_)

    def commit(self):
        self.data['_from'] = self.from_.id_
        self.data['_to'] = self.to_.id_

        if self.id_:
            self.http_client.graph.replace_edge(self.graph_name, self.collection_name, self.id_, self.data)
        else:
            result = self.http_client.graph.create_edge(self.graph_name, self.collection_name, self.data)
            self.id_ = result['edge']['_id']
            self.key_ = result['edge']['_key']
            self.rev_ = result['edge']['_rev']


class VertexCollection(Collection):
    def __init__(self, http_client, database, graph_name, collection_name, new=False):
        super().__init__(http_client, database, collection_name, new=new)
        self.graph_name = graph_name

    def create_vertex(self, data):
        vertex = Vertex(self, data=data)
        self._cached_documents.append(vertex)
        return vertex

    def get_vertex(self, vertex_key):
        vertex = Vertex(self, id_=vertex_key)
        self._cached_documents.append(vertex)
        return vertex


class EdgeCollection(Collection):
    def __init__(self, http_client, database, graph_name, collection_name, new=False):
        super().__init__(http_client, database, collection_name, new=new)
        self.graph_name = graph_name

    def create_edge(self, source, destination, data):
        edge = Edge(self, source, destination, data=data)
        self._cached_documents.append(edge)
        return edge

    def get_edge(self, edge_key):
        edge = Edge(self, None, None, id_=edge_key)
        self._cached_documents.append(edge)
        return edge


class Graph(Writable):

    def __init__(self, http_client, database, name, new=False):
        self.http_client = http_client
        self.database = database
        self.id_ = None
        self.rev_ = None
        self.name = name

        self.is_new = new
        self.vertex_collections = dict()
        self.edge_collections = dict()

        if not new:
            self._populate()

    def _populate(self):
        info = self.http_client.graph.get(self.name)
        self.id_ = info['_id']
        self.rev_ = info['_rev']

        vertex_collection_names = list()
        for vertex_def in info.get('orphan_collections', list()):
            vertex_collection_names.append(vertex_def['collection'])
        for edge_def in info.get('edge_definitions', list()):
            self.edge_collections[edge_def['collection']] = EdgeCollection(self.http_client, self.database, self.name,
                                                                           edge_def['collection'])
            for from_collection in edge_def['from']:
                vertex_collection_names.append(from_collection)
            for to_collection in edge_def['to']:
                vertex_collection_names.append(to_collection)

        for vertex_collection in set(vertex_collection_names):
            self.vertex_collections[vertex_collection] = VertexCollection(self.http_client, self.database, self.name,
                                                                          vertex_collection)

    def create_edge(self, edge_collection, source, destination, data):
        return self.edge_collections[edge_collection].create_edge(source, destination, data)

    def create_vertex(self, vertex_collection, data):
        return self.vertex_collections[vertex_collection].create_vertex(data)

    def commit(self):
        for vertex_collection in self.vertex_collections.values():
            vertex_collection.commit()
        for edge_collection in self.edge_collections.values():
            edge_collection.commit()
