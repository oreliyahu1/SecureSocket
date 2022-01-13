import abc
from typing import TypeVar, Generic

T = TypeVar('T')
G = TypeVar('G')


class ICryptoMessage(Generic[T, G], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, crp_msg: T, msg_signature: G = None):
        raise NotImplementedError('ICryptoMessage: __init__ function is not defined')

    @abc.abstractmethod
    def get_dict_message(self) -> dict:
        raise NotImplementedError('ICryptoMessage: get_dict_message function is not defined')

    @abc.abstractmethod
    def get_message(self) -> T:
        raise NotImplementedError('ICryptoMessage: get_message function is not defined')

    @abc.abstractmethod
    def get_signature(self) -> G:
        raise NotImplementedError('ICryptoMessage: get_message function is not defined')