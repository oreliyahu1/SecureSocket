import unittest
import os
import hashlib
from random import randrange
from Crypto.DigitalSignature.ElGamalDigitalSignature import ElGamalDigitalSignature


class ElGamalTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ElGamalTest, self).__init__(*args, **kwargs)

    def test_elgamal_1(self):
        eg_ds = ElGamalDigitalSignature('sha1')
        (s1, s2) = eg_ds.get_signature("a234444234fsd")
        (v1, v2) = eg_ds.get_verification([s1, s2], "a234444234fsd")
        self.assertEqual(v1, v2)
        self.assertEqual(eg_ds.verification([v1, v2]), True)

    def test_elgamal_2(self):
        eg_ds = ElGamalDigitalSignature('sha1')
        (s1, s2) = eg_ds.get_signature("a234444234fsd")
        (v1, v2) = eg_ds.get_verification([s1, s2], "111a234444234fsd")
        self.assertNotEqual(v1, v2)
        self.assertEqual(eg_ds.verification([v1, v2]), False)

    def test_elgamal_3(self):
        eg_ds = ElGamalDigitalSignature('md5')
        (s1, s2) = eg_ds.get_signature("a234444234fsd")
        (v1, v2) = eg_ds.get_verification([s1, s2], "a234444234fsd")
        self.assertEqual(v1, v2)
        self.assertEqual(eg_ds.verification([v1, v2]), True)

    def test_elgamal_4(self):
        eg_ds = ElGamalDigitalSignature('md5')
        (s1, s2) = eg_ds.get_signature("a234444234fsd")
        (v1, v2) = eg_ds.get_verification([s1, s2], "111a234444234fsd")
        self.assertNotEqual(v1, v2)
        self.assertEqual(eg_ds.verification([v1, v2]), False)

if __name__ == '__main__':
    unittest.main()
