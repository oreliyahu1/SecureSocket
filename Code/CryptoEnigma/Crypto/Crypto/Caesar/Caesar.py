from typing import List

from ICrypto.IKey import IKey
from ICrypto.ICrypto import ICrypto


class Caesar(ICrypto[str, List[str]]):

    def __init__(self, key: IKey[int]):
        self.key = None
        self.set_key(key)

    def set_key(self, key: IKey[int]):
        self.key = key.get_key('key')

    def encryption(self, pain_text: str) -> List[str]:
        cipher_text = []
        for c in pain_text:
            cipher_text += [hex((ord(c) + self.key) % 256)]

        return cipher_text

    def decryption(self, cipher_text: List[str]) -> str:
        pain_text = ''
        for c in cipher_text:
            pain_text += chr((int(c, 16) - self.key) % 256)

        return pain_text
