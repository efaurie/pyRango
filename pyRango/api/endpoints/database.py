from pyRango.api.endpoints.meta import Endpoint, ArangoError


class DatabaseEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/database'

    def current(self):
        return self.get(self.build_uri('current'))

    def list(self):
        return self.get(self.build_uri())

    def list_accessible(self):
        return self.get(self.build_uri('user'))

    def create(self, name, users=None):
        payload = {'name': name}
        if users:
            payload['users'] = users

        return self.post(self.build_uri(), payload=payload)

    def delete(self, name):
        if self.client.current_database != '_system':
            raise ArangoError('You can only drop databases from within the _system database.')
        return self.delete(self.build_uri(name))

