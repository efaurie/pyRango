from pyRango.api.endpoints.meta import Endpoint


class TraversalEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/traversal'

    @classmethod
    def check_and_set_direction(cls, direction, parameters):
        if direction.lower() not in ['outbound', 'inbound', 'any']:
            parameters['direction'] = 'outbound'  # Default
        else:
            parameters['direction'] = direction.lower()

    @classmethod
    def check_and_set_strategy(cls, strategy, parameters):
        if strategy.lower() not in ['depthfirst', 'breadthfirst']:
            parameters['strategy'] = 'breadthfirst'
        else:
            parameters['strategy'] = strategy.lower()

    @classmethod
    def check_and_set_order(cls, order, parameters):
        if order.lower() not in ['preorder', 'postorder', 'preorder-expander']:
            parameters['order'] = 'preorder'
        else:
            parameters['order'] = order.lower()

    def filter_parameters(self, graph_name, edge_collection, start_vertex, kwargs):
        parameters = {
            'graph_name': graph_name,
            'edge_collection': edge_collection,
            'start_vertex': start_vertex
        }

        if 'direction' in kwargs:
            self.check_and_set_direction(kwargs['direction'], parameters)
        if 'min_depth' in kwargs:
            parameters['min_depth'] = kwargs['min_depth']
        if 'strategy' in kwargs:
            self.check_and_set_strategy(kwargs['strategy'], parameters)
        if 'max_iterations' in kwargs:
            parameters['max_iterations'] = kwargs['max_iterations']
        if 'max_depth' in kwargs:
            parameters['max_depth'] = kwargs['max_depth']
        if 'order' in kwargs:
            self.check_and_set_order(kwargs['order'], parameters)

        return parameters

    def execute(self, graph_name, edge_collection, start_vertex, **kwargs):
        parameters = self.filter_parameters(graph_name, edge_collection, start_vertex, kwargs)
        self._post(self.build_uri(), payload=parameters)
