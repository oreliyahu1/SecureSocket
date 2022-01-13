import abc
from ICrypto import ICrypto, IKeyExchange
from typing import TypeVar, Generic

T = TypeVar('T')
G = TypeVar('G')


class IKeyExchangeGenerator(Generic[T, G], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, crp: ICrypto, key_exchange: IKeyExchange):
        raise NotImplementedError('IKeyExchangeGenerator: __init__ function is not defined')

    @abc.abstractmethod
    def generate_message(self, pain_text: T) -> G:
        raise NotImplementedError('ICryptoMessageGenerator: generate_message function is not defined')

    @abc.abstractmethod
    def degenerate_message(self, c_msg: G) -> T:
        raise NotImplementedError('ICryptoMessageGenerator: degenerate_message function is not defined')

    @abc.abstractmethod
    def get_crypto(self) -> ICrypto:
        raise NotImplementedError('ICryptoMessageGenerator: get_crypto function is not defined')

    @abc.abstractmethod
    def set_crypto(self, crp: ICrypto):
        raise NotImplementedError('ICryptoMessageGenerator: set_crypto function is not defined')

    def set_key_exchange(self, key_exchange: IKeyExchange):
        raise NotImplementedError('ICryptoMessageGenerator: set_key_exchange function is not defined')

    def get_key_exchange(self) -> IKeyExchange:
        raise NotImplementedError('ICryptoMessageGenerator: get_key_exchange function is not defined')