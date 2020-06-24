import abc
from ICrypto.IKey import IKey
from typing import List, TypeVar, Generic

T = TypeVar('T')
G = TypeVar('G')


class ICrypto(Generic[T, G], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, key: IKey = None):
        raise NotImplementedError('ICrypto: __init__ function is not defined')

    @abc.abstractmethod
    def set_key(self, key: IKey):
        raise NotImplementedError('ICrypto: set_key function is not defined')

    @abc.abstractmethod
    def encryption(self, pain_text: T) -> G:
        raise NotImplementedError('ICrypto: encryption function is not defined')

    @abc.abstractmethod
    def decryption(self, cipher_text: G) -> T:
        raise NotImplementedError('ICrypto: decryption function is not defined')