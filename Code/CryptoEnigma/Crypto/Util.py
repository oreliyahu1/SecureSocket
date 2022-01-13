import random
import math
from typing import List


class Util:

    @staticmethod
    def padding_hex_list(text: List[chr], padding_size: int) -> List[chr]:
        #0x00 esc #0x01 flag
        padding_text = []
        if padding_size:
            text.insert(len(text) - padding_size, '_')
        for c in text:
            if c == '0x00' or c == '0x01':
                padding_text.append('0x00')
            if c != '_':
                padding_text.append(c)
            else:
                padding_text.append('0x01')
        return padding_text

    @staticmethod
    def unpadding_hex_list(text: List[chr]) -> (List[chr], int):
        padding_size, padding_esc, padding_flag, unpadding_text = 0, False, False, []
        for c in text:
            if c == '0x00' and not padding_esc:
                padding_esc = True
            else:
                if padding_esc and (c == '0x00' or c == '0x01'):
                    padding_esc = False
                    unpadding_text.append(c)
                elif c == '0x01':
                    padding_flag = True
                    padding_size = -1
                else:
                    unpadding_text.append(c)
                if padding_flag:
                    padding_size += 1
        return unpadding_text, padding_size

    @staticmethod
    def gcd(a, b) -> int:
        if a < b:
            return Util.gcd(b, a)
        elif a % b == 0:
            return b
        else:
            return Util.gcd(b, a % b)

    @staticmethod
    def get_prime(r_min: int = pow(10, 5), r_max: int = pow(10, 8)) -> int:
        while True:
            prime = random.randint(r_min, r_max)
            if Util.is_prime(prime):
                return prime

    @staticmethod
    def is_prime(num: int) -> bool:
        upto = int(math.sqrt(num)) + 1
        for n in range(2, upto):
            if Util.gcd(num, n) > 1:
                return False
        return True

    @staticmethod
    def iterative_egcd(a: int, b: int) -> (int, int, int):
        x, y, u, v = 0, 1, 1, 0
        while a != 0:
            q, r = b // a, b % a
            m, n = x - u * q, y - v * q  # use x//y for floor "floor division"
            b, a, x, y, u, v = a, r, u, v, m, n
        return b, x, y

    @staticmethod
    # return ki => ki**-1 * k = 1 mod q
    def modinv(k: int, q: int):
        g, x, y = Util.iterative_egcd(k, q)
        if g != 1:
            return None
        else:
            return x % q

    # such that create_pair_prime_and_generator() will return (q,a) containing a safe prime q with
    # and a generator a for Z∗q.
    @staticmethod
    def create_pair_prime_and_generator() -> (int, int):
        safe_prime = 0
        while True:
            q = Util.get_prime()
            safe_prime = 2 * q + 1
            if Util.is_prime(safe_prime):
                break
        while True:
            a = random.randint(2, safe_prime - 1)
            if (safe_prime - 1) % a != 1:
                break

        return safe_prime, a