import abc
from ICrypto.IKey import IKey
from typing import TypeVar, Generic

G = TypeVar('G')


class IKeyExchange(Generic[G], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, key: IKey = None):
        raise NotImplementedError('IKeyExchange: __init__ function is not defined')

    @abc.abstractmethod
    def set_key(self, key: IKey):
        raise NotImplementedError('IKeyExchange: set_key function is not defined')

    @abc.abstractmethod
    def get_key(self) -> IKey:
        raise NotImplementedError('IKeyExchange: get_key function is not defined')

    @abc.abstractmethod
    def get_k(self) -> G:
        raise NotImplementedError('IKeyExchange: get_k function is not defined')