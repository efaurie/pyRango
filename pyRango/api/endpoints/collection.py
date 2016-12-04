import re
import logging

from pyRango.api.endpoints.meta import Endpoint, ArangoError

LOG = logging.getLogger(__name__)


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

        kwargs['name'] = name

        return self._post(self.build_uri(), payload=kwargs)

    def list(self, exclude_system=False):
        return self._get(self.build_uri(), exclude_system=exclude_system)

    def get(self, name, *args, singleton_list=False):
        """
        Parameters
        ----------
        name : str
            The name of a collection you wish to get information for.
        args : list of str (optional)
            Any subsequent collections you would also wish to get information for.
        singleton_list : bool (optional)
            Whether a result of length one should be returned as a singleton list or not.
            This arg only applies to specifically listed collections
        """
        results = [self._get(self.build_uri(name))]
        for collection_name in args:
            results.append(self._get(self.build_uri(collection_name)))

        if not singleton_list and len(results) == 1:
            return results[0]
        else:
            return results

    def get_properties(self, name):
        return self._get(self.build_uri(name, 'properties'))

    def get_document_count(self, name):
        return self._get(self.build_uri(name, 'count'))

    def get_statistics(self, name):
        return self._get(self.build_uri(name, 'figures'))

    def get_revision(self, name):
        return self._get(self.build_uri(name, 'revision'))

    def get_checksum(self, name, with_revisions=False, with_data=False):
        """
        Parameters
        ----------
        name : str
            The name of the collection to get the checksum of
        with_revisions : bool (optional)
            Whether or not to include document IDs in the Checksum calculation.
        with_data : bool (optional)
            Whether or not to include document body data in the checksum calculation.

        """
        return self._get(self.build_uri(name, 'checksum'), with_revisions=with_revisions, with_data=with_data)

    def load(self, name):
        return self._put(self.build_uri(name, 'load'))

    def unload(self, name):
        return self._put(self.build_uri(name, 'unload'))

    def set_properties(self, name, wait_for_sync=None, journal_size=None):
        if not wait_for_sync and not journal_size:
            LOG.warning('[!] No-Op collection.set_properties call as neither arg was specified')
            return dict()
        payload = {}
        if wait_for_sync:
            payload['wait_for_sync'] = wait_for_sync
        if journal_size:
            payload['journal_size'] = journal_size

        return self._put(self.build_uri(name, 'properties'), payload=payload)

    def rename(self, old_name, new_name):
        return self._put(self.build_uri(old_name, 'rename'), payload={'name': new_name})

    def rotate(self, name):
        return self._put(self.build_uri(name, 'rotate'))

    def delete(self, name):
        return self._delete(self.build_uri(name))
