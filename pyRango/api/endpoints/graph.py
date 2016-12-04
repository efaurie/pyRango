from pyRango.api.endpoints.meta import Endpoint


class GraphEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/gharial'

    def list(self):
        return self._get(self.build_uri())

    def create(self, name, edge_definitions, orphan_collections):
        payload = {
            'name': name,
            'edge_definitions': edge_definitions,
            'orphan_collections': orphan_collections
        }
        return self._post(self.build_uri(), payload=payload)

    def get(self, name):
        return self._get(self.build_uri(name))

    def delete(self, name, drop_collections=False):
        return self._delete(self.build_uri(name), payload={'drop_collections': drop_collections})

    def list_vertex_collections(self, graph_name):
        return self._get(self.build_uri(graph_name, 'vertex'))

    def add_vertex_collection(self, graph_name, collection_name):
        return self._post(self.build_uri(graph_name, 'vertex'), payload={'collection': collection_name})

    def delete_vertex_collection(self, graph_name, collection_name):
        return self._delete(self.build_uri(graph_name, 'vertex', collection_name), payload={'drop_collection': True})

    def remove_vertex_collection(self, graph_name, collection_name):
        return self._delete(self.build_uri(graph_name, 'vertex', collection_name))

    def list_edge_collections(self, graph_name):
        return self._get(self.build_uri(graph_name, 'edge'))

    def add_edge_collection(self, graph_name, collection_name, to_vertices, from_vertices):
        payload = {
            'collection': collection_name,
            'to': to_vertices,
            'from': from_vertices
        }
        return self._post(self.build_uri(graph_name, 'edge'), payload=payload)

    def replace_edge_collection(self, graph_name, old_collection_name, new_collection_name, to_vertices, from_vertices):
        payload = {
            'collection': new_collection_name,
            'to': to_vertices,
            'from': from_vertices
        }
        return self._put(self.build_uri(graph_name, old_collection_name), payload=payload)

    def delete_edge_collection(self, graph_name, collection_name):
        return self._delete(self.build_uri(graph_name, collection_name), payload={'drop_collection': True})

    def remove_edge_collection(self, graph_name, collection_name):
        return self._delete(self.build_uri(graph_name, collection_name))

    def create_vertex(self, graph_name, collection_name, document):
        payload = {'storeThisObject': document}
        return self._post(self.build_uri(graph_name,  'vertex', collection_name), payload=payload, transform=False)

    def get_vertex(self, graph_name, collection_name, vertex_key):
        return self._get(self.build_uri(graph_name,  'vertex', collection_name, vertex_key))

    def modify_vertex(self, graph_name, collection_name, vertex_key, new_values):
        payload = {'replaceAttributes': new_values}
        return self._patch(self.build_uri(graph_name,  'vertex', collection_name, vertex_key), payload=payload,
                           transform=False)

    def replace_vertex(self, graph_name, collection_name, vertex_key, new_document):
        payload = {'storeThisJsonObject': new_document}
        return self._put(self.build_uri(graph_name,  'vertex', collection_name, vertex_key), payload=payload,
                         transform=False)

    def delete_vertex(self, graph_name, collection_name, vertex_key):
        return self._delete(self.build_uri(graph_name, 'vertex', collection_name, vertex_key))

    def create_edge(self, graph_name, collection_name, document):
        payload = {'storeThisJsonObject': document}
        return self._post(self.build_uri(graph_name, 'edge', collection_name), payload=payload, transform=False)

    def get_edge(self, graph_name, collection_name, edge_key):
        return self._get(self.build_uri(graph_name, 'edge', collection_name, edge_key))

    def modify_edge(self, graph_name, collection_name, edge_key, new_values):
        payload = {'updateAttributes': new_values}
        return self._patch(self.build_uri(graph_name, 'edge', collection_name, edge_key), payload=payload,
                           transform=False)

    def replace_edge(self, graph_name, collection_name, edge_key, new_document):
        payload = {'storeThisJsonObject': new_document}
        return self._put(self.build_uri(graph_name, 'edge', collection_name, edge_key), payload=payload,
                         transform=False)

    def delete_edge(self, graph_name, collection_name, edge_key):
        return self._delete(self.build_uri(graph_name, collection_name, edge_key))
