import string
from ICrypto.IKey import IKey
from typing import List, TypeVar

T = TypeVar('T')


class Key(IKey[T]):

    def __init__(self, keys=None):
        if keys is None:
            keys = dict()
        self.keys = keys

    def set_key(self, key_name: string, key: T):
        self.keys[key_name] = key

    def get_key(self, key_name: string) -> T:
        return self.keys.get(key_name)

    def get_keys_name(self) -> List[str]:
        return list(self.keys.keys())

    def size(self) -> int:
        return len(self.keys)