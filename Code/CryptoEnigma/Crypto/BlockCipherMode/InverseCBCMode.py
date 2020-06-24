from ICrypto.ICryptoWMode import ICryptoWMode
from ICrypto.ICrypto import ICrypto
from ICrypto.IKey import IKey
from Crypto.BlockCipherMode.CBCMode import CBCMode
from Crypto.Util import Util
from typing import List


class InverseCBCMode(ICryptoWMode[str, List[chr]]):

    def __init__(self, crp: ICrypto, m_key: IKey[str]):
        self.enigma_cbc_mode = CBCMode(crp, m_key, '')
        self.crp = crp
        self.set_key(m_key)

    def set_key(self, m_key: IKey[str]):
        self.enigma_cbc_mode.set_key(m_key)

    def set_crypto(self, crp: ICrypto):
        self.enigma_cbc_mode.set_crypto(crp)

    def encryption(self, pain_text: str) -> List[chr]:
        cipher_text = []
        padding_size = (-len(pain_text) % len(self.enigma_cbc_mode.m_key))
        pain_text += padding_size * 'F'
        temp = self.enigma_cbc_mode.decryption(list(pain_text))
        for c in temp:
            cipher_text.append(hex(ord(c)))
        return Util.padding_hex_list(cipher_text, padding_size)

    def decryption(self, cipher_text: List[chr]) -> str:
        (padding_cipher_text, padding_size) = Util.unpadding_hex_list(cipher_text)
        pain_text = []
        for c in padding_cipher_text:
            pain_text.append(chr(int(c, 16)))
        pain_text = self.enigma_cbc_mode.encryption(pain_text)
        if padding_size:
            pain_text = pain_text[:-padding_size]
        return ''.join(pain_text)
