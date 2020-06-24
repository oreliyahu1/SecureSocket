from ICrypto.IKeyExchangeGenerator import IKeyExchangeGenerator
from ICrypto.ICrypto import ICrypto
from ICrypto.IKeyExchange import IKeyExchange

from typing import TypeVar, Generic

T = TypeVar('T')
G = TypeVar('G')


class KeyExchangeGenerator(IKeyExchangeGenerator[T, G]):

    def __init__(self, crp: ICrypto, key_exchange: IKeyExchange):
        self.crp = crp
        self.key_exchange = key_exchange

    def generate_message(self, pain_text: T) -> G:
        cipher_text = self.crp.encryption(pain_text)
        return cipher_text

    def degenerate_message(self, c_msg: G) -> T:
        return self.crp.decryption(c_msg)

    def get_crypto(self) -> ICrypto:
        return self.crp

    def set_crypto(self, crp: ICrypto):
        self.crp = crp

    def set_key_exchange(self, key_exchange: IKeyExchange):
        self.key_exchange = key_exchange

    def get_key_exchange(self) -> IKeyExchange:
        return self.key_exchange
