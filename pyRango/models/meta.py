import abc


class Writable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError()
