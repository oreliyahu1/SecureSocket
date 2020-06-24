import abc
from typing import TypeVar, Generic

T = TypeVar('T')
S = TypeVar('S')


class ISignature(Generic[T, S], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_signature(self, M: T) -> S:
        raise NotImplementedError('ISignature: get_message function is not defined')

    @abc.abstractmethod
    def get_verification(self, signature: S, M: T) -> S:
        raise NotImplementedError('ISignature: get_verification function is not defined')

    @abc.abstractmethod
    def verification(self, out_ver: S) -> bool:
        raise NotImplementedError('ISignature: verification function is not defined')
