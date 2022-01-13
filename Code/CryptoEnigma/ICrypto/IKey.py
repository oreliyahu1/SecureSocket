import abc
from typing import List, TypeVar, Generic

T = TypeVar('T')


class IKey(Generic[T], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, keys):
        raise NotImplementedError('IKey: __init__ function is not defined')

    @abc.abstractmethod
    def set_key(self, key_name: str, key: T):
        raise NotImplementedError('IKey: set_key function is not defined')

    @abc.abstractmethod
    def get_key(self, key_name: str) -> T:
        raise NotImplementedError('IKey: get_key function is not defined')

    @abc.abstractmethod
    def get_keys_name(self) -> List[str]:
        raise NotImplementedError('IKey: get_keys_name function is not defined')

    @abc.abstractmethod
    def size(self) -> int:
        raise NotImplementedError('IKey: size function is not defined')