import random

from ICrypto.IKey import IKey
from ICrypto.IKeyExchange import IKeyExchange
from Crypto.Util import Util


class DiffieHellman(IKeyExchange[int]):

    def __init__(self, key: IKey[int] = None):
        self.n, self.g, self.gy = None, None, None
        if key is None:
            self.n, self.g = Util.create_pair_prime_and_generator()
        else:
            self.set_key(key)
        self.x = random.randint(2, self.n - 1)
        self.gx = pow(self.g, self.x, self.n)

    def set_key(self, key: IKey[int]):
        if key.get_key('n') and self.n is None:
            self.n = key.get_key('n')
        if key.get_key('g') and self.g is None:
            self.g = key.get_key('g')
        if key.get_key('gi') and self.gy is None:
            self.gy = key.get_key('gi')

    def get_key(self) -> dict:
        return {'n': self.n, 'g': self.g, 'gi': self.gx}

    def get_k(self) -> int:
        return pow(self.gy, self.x, self.n)
