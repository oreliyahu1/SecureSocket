import random
from Crypto.Key import Key
from Crypto.Util import Util
from ICrypto.ISignature import ISignature
from ICrypto.IKey import IKey
from typing import List
import hashlib


class ElGamalDigitalSignature(ISignature[str, List[int]]):

    def __init__(self, hash_function_name: str, public_keys: IKey[int] = None):
        if public_keys is None:
            self.private_keys, self.public_keys = self.creates_keys()
        else:
            self.private_keys = None
            self.public_keys = public_keys

        hashlib.new(hash_function_name)
        self.hash_function_name = hash_function_name

    def get_public_keys(self) -> IKey:
        return self.public_keys

    def get_signature(self, M: str) -> List[int]:
        if self.private_keys is None:
            raise ValueError('ElGamalDigitalSignature get_signature: cannot create signature in public mode')
        h = hashlib.new(self.hash_function_name)
        h.update(M.encode())
        m = int(h.hexdigest(), 35)

        while 1:
            k = random.randint(1, self.private_keys.get_key('q') - 2)
            if Util.gcd(k, self.private_keys.get_key('q') - 1) == 1:
                break
        s1 = pow(self.private_keys.get_key('a'), k, self.private_keys.get_key('q'))
        ki = Util.modinv(k, self.private_keys.get_key('q') - 1)
        s2 = ki * (m - self.private_keys.get_key('Xa') * s1) % (self.private_keys.get_key('q') - 1)
        return [s1, s2]

    def get_verification(self, signature: List[int], M: str) -> List[int]:
        h = hashlib.new(self.hash_function_name)
        h.update(M.encode())
        m = int(h.hexdigest(), 35)
        s1, s2 = signature[0], signature[1]

        if s1 < 1 or s1 > self.public_keys.get_key('q') - 1:
            return [1, 0]
        v1 = pow(self.public_keys.get_key('Ya'), s1, self.public_keys.get_key('q')) % self.public_keys.get_key('q') * pow(s1, s2, self.public_keys.get_key('q')) % self.public_keys.get_key('q')
        v2 = pow(self.public_keys.get_key('a'), m, self.public_keys.get_key('q'))
        return [v1, v2]

    def verification(self, out_ver: List[int]) -> bool:
        return out_ver[0] == out_ver[1]

    @staticmethod
    def creates_keys() -> (IKey[int], IKey[int]):
        eg_private_keys = Key[int]()
        eg_public_keys = Key[int]()
        q, a = Util.create_pair_prime_and_generator()
        xa = random.randint(1, q - 2)
        ya = pow(a, xa, q)
        eg_private_keys.set_key('q', q)
        eg_private_keys.set_key('a', a)
        eg_private_keys.set_key('Xa', xa)
        eg_private_keys.set_key('Ya', ya)
        eg_public_keys.set_key('q', q)
        eg_public_keys.set_key('a', a)
        eg_public_keys.set_key('Ya', ya)
        return eg_private_keys, eg_public_keys
