from ICrypto.ICryptoWMode import ICryptoWMode
from ICrypto.ICrypto import ICrypto
from ICrypto.IKey import IKey
from typing import List


class CBCMode(ICryptoWMode[List[chr], List[chr]]):

    def __init__(self, crp: ICrypto, m_key: IKey[str], missing_char: chr = '0'):
        self.crp = crp
        self.m_key = []
        self.set_key(m_key)
        self.missing_char = missing_char

    def set_key(self, m_key: IKey[str]):
        if m_key is None or m_key.size() == 0 or m_key.get_key('cbc_key') is None:
            raise ValueError('CBCMode: m_key must to be with value')
        self.m_key = self.key_to_cbc_key(m_key.get_key('cbc_key'))

    @staticmethod
    def key_to_cbc_key(m_key: str):
        if m_key is None:
            raise ValueError('CBCMode: key_to_cbc_key must to be with value')
        l_m_key = []
        for i, c in enumerate(m_key):
            l_m_key.append(hex(ord(c) % 256))
        return l_m_key

    def set_crypto(self, crp: ICrypto):
        self.crp = crp

    def encryption(self, pain_text: List[chr]) -> List[chr]:
        if not pain_text: return ''
        cipher_text = []
        pain_text_blocks = [pain_text[index: index + len(self.m_key)] for index in
                            range(0, len(pain_text), len(self.m_key))]
        pain_text_blocks[len(pain_text_blocks) - 1] += (len(self.m_key) - len(
            pain_text_blocks[len(pain_text_blocks) - 1])) * self.missing_char
        iv = list(self.m_key)
        for i, pain_text_block in enumerate(pain_text_blocks):
            xor_text_block = ''
            for j, c in enumerate(pain_text_block):
                xor_text_block += chr(int(iv[j], 16) ^ ord(c))
            cipher_text_en = self.crp.encryption(xor_text_block)
            iv = self.key_to_cbc_key(cipher_text_en) #iv[i+1] = E[p[i] ^ iv[i]]
            cipher_text += cipher_text_en
        return cipher_text

    def decryption(self, cipher_text: List[chr]) -> List[chr]:
        if cipher_text is None: return ''
        pain_text = []
        cipher_text = [cipher_text[i:i + len(self.m_key)] for i in
                              range(0, len(cipher_text), len(self.m_key))]
        if len(cipher_text[len(cipher_text) - 1]) != len(self.m_key):
            raise ValueError('CBCMode_decryption: ciper_text doesnt match to block size')

        iv = list(self.m_key)
        for i, cipher_text_block in enumerate(cipher_text):
            cipher_text_en = self.crp.decryption(''.join(cipher_text_block))
            xor_text_block = ''
            for j, c in enumerate(cipher_text_en):
                xor_text_block += chr(int(iv[j], 16) ^ ord(c))
            iv = self.key_to_cbc_key(''.join(cipher_text_block)) #iv[i+1] = C[i]
            pain_text += xor_text_block

        return pain_text
