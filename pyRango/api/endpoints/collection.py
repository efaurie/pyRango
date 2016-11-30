import re

from pyRango.utils import dict_to_camel
from pyRango.api.endpoints.meta import Endpoint, ArangoError


class CollectionEndpoint(Endpoint):
    def __init__(self, client):
        super().__init__(client)
        self.suffix = '_api/collection'

    @classmethod
    def is_valid(cls, name, system_collection=False):
        is_valid = re.fullmatch(r'^[a-zA-Z0-9_-]*$', name)
        if system_collection and not name.startswith('_'):
            is_valid = False
        return is_valid

    def list(self):
        return self.get(self.build_uri())

    def create(self, name, **kwargs):
        """

        Parameters
        ----------
        name : String
            The name of the new collection (Must contain only letters, digits, _ or -)
        kwargs : dict (Optional)
            journal_size : int
                The max size of the Journal or Datafile in bytes. (Must be at least 1 MB)
            replication_factory : int
                The number of copies of each shard to distribute to different nodes.
            key_options : dict
                allow_user_keys : boolean
                    Whether or not to allow users to specify their own _key on documents.
                type : string
                    Which key generator to use -- one of 'traditional' or 'autoincrement'
                increment : int
                    The increment value to use if 'autoincrement' is set.
                offset : int
                    The initial offset of the 'autoincrement' generator.
            wait_for_sync : boolean
                Whether the server should wait for a write before returning from a document create call (Default: false)
            do_compact : boolean
                Whether or not the collection will be compacted (Default: true)
            is_volatile : boolean
                Whether or not the collection is kept only in memory - IE: Not written to disk (Default: false)
            shard_keys : list of string
                Which field to hash on when determining which shard to allocate the document to. (Default: _key)
            number_of_shards : int
                The number of shards to create for the collection when in a cluster (Default: 1)
            is_system : boolean
                Whether to create the collection as a system level collection or not. System level collections should
                always begin with an underscore (Default: false)
            type : int
                The type of the collection to make (2 = Document Collection, 3 = Edge Collection)
            index_buckets : int
                The number of buckets to split a hash-based index into - Must be a power of 2 (Default: 16)

        Returns
        -------
        dict
        """
        if not self.is_valid(name):
            raise ArangoError('Collection Name Invalid: It must only contain letters, digits, _ or -')

        payload = dict_to_camel(kwargs)
        payload['name'] = name

        return self.post(self.build_uri(), payload=payload)

    def delete(self, name):
        return self.delete(self.build_uri(name))
