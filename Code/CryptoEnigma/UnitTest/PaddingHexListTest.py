import unittest
from Crypto.Util import Util

class MyTestCase(unittest.TestCase):

    def test_padding_hex_list_1(self):
        text = ['0x00', '0x11', '0x01', '0x13'] + 10 * ['0x00'] + 10 * ['0x01']
        a = Util.padding_hex_list(list(text), 4)
        b, c = Util.unpadding_hex_list(a)
        self.assertEqual(text, b)
        self.assertEqual(c, 4)

    def test_padding_hex_list_2(self):
        text = ['0x00', '0x11', '0x01', '0x13'] + 10 * ['0x00'] + 10 * ['0x01']
        a = Util.padding_hex_list(list(text), 10)
        b, c = Util.unpadding_hex_list(a)
        self.assertEqual(text, b)
        self.assertEqual(c, 10)

    def test_padding_hex_list_3(self):
        text = ['0x00', '0xff', '0x01', '0xff', '0x01', '0xff', '0x01', '0x13']
        a = Util.padding_hex_list(list(text), 0)
        b, c = Util.unpadding_hex_list(a)
        self.assertEqual(text, b)
        self.assertEqual(c, 0)

if __name__ == '__main__':
    unittest.main()
