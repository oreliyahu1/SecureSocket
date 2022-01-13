import unittest
from Crypto.KeyExchange.DiffieHellman import DiffieHellman
from Crypto.Key import Key


class DiffieHellmanTest(unittest.TestCase):

    def test_dh_1(self):
        dh = DiffieHellman()
        self.assertEqual(None, dh.gy)
        self.assertNotEqual(None, dh.n)
        self.assertNotEqual(None, dh.g)
        self.assertNotEqual(None, dh.x)
        self.assertNotEqual(None, dh.gx)

    def test_dh_2(self):
        dh = DiffieHellman()
        try:
            self.assertEqual(None, dh.get_k())
        except TypeError as te:
            self.assertTrue(True)

    def test_dh_3(self):
        dh = DiffieHellman()
        dh_2 = DiffieHellman(Key[int](dh.get_key()))
        dh.set_key(Key[int](dh_2.get_key()))
        self.assertEqual(dh.get_k(), dh_2.get_k())

    def test_dh_4(self):
        dh = DiffieHellman()
        dh_2 = DiffieHellman(Key[int](dh.get_key()))
        dh.set_key(Key[int](dh_2.get_key()))

        self.assertEqual(dh.n, dh_2.n)
        self.assertEqual(dh.g, dh_2.g)
        self.assertNotEqual(dh.x, dh_2.x)
        self.assertNotEqual(dh.gx, dh_2.gx)
        self.assertEqual(dh.gy, dh_2.gx)


if __name__ == '__main__':
    unittest.main()
