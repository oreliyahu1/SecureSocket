import abc
import string
from ICrypto.ICrypto import ICrypto
from ICrypto.IKey import IKey
from typing import TypeVar, Generic

T = TypeVar('T')
G = TypeVar('G')


class ICryptoWMode(ICrypto[T, G], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, crp: ICrypto, m_key: IKey = None, missing_char: chr = '0'):
        raise NotImplementedError('ICryptoWMode: __init__ function is not defined')

    @abc.abstractmethod
    def set_key(self, m_key: IKey):
        raise NotImplementedError('ICryptoWMode: set_key function is not defined')

    @abc.abstractmethod
    def set_crypto(self, crp: ICrypto):
        raise NotImplementedError('ICryptoWMode: set_crypto function is not defined')

    @abc.abstractmethod
    def encryption(self, pain_text: T) -> G:
        raise NotImplementedError('ICryptoWMode: encryption function is not defined')

    @abc.abstractmethod
    def decryption(self, cipher_text: G) -> T:
        raise NotImplementedError('ICryptoWMode: decryption function is not defined')