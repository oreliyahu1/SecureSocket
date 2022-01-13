import unittest

from Crypto.Crypto.Enigma.Enigma import Enigma
from Crypto.Crypto.Enigma.PlugBoard import PlugBoard
from Crypto.Crypto.Enigma.Reflector import Reflector
from Crypto.Crypto.Enigma.Rotor import Rotor
from Crypto.Crypto.Enigma.RotorMechanism import RotorMechanism
from Crypto.Crypto.Enigma.EnigmaSettings import EnigmaSettings
from Crypto.Crypto.Enigma.EnigmaStatic import az_to_index, index_to_az, valid_character
from Crypto.BlockCipherMode.InverseCBCMode import InverseCBCMode
from Crypto.Key import Key


class CryptoEnigmaTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(CryptoEnigmaTest, self).__init__(*args, **kwargs)

    def test_az_to_index(self):
        for c in range(0, 26):
            self.assertEqual(c, az_to_index(chr(c + ord('A'))))
        try:
            az_to_index('4')
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('EnigmaStatic_valid_character: unexpected character, enigma only supports A-Z characters')))
        try:
            az_to_index(None)
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('EnigmaStatic_valid_character: unexpected character, enigma only supports A-Z characters')))

    def test_index_to_az(self):
        for c in range(0, 26):
            self.assertEqual(c, az_to_index(index_to_az(c)))

        try:
            index_to_az(-1)
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('EnigmaStatic_index_to_az: unexpected index, enigma only supports 0-25 index\'s')))

    def test_valid_character(self):
        for c in range(0, 26):
            self.assertEqual(True, valid_character(chr(c + ord('A'))))
        try:
            valid_character('4', True)
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('EnigmaStatic_valid_character: unexpected character, enigma only supports A-Z characters')))
        try:
            valid_character(None, True)
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('EnigmaStatic_valid_character: unexpected character, enigma only supports A-Z characters')))
        self.assertEqual(False, valid_character('4'))

    def test_plug_board_1(self):
        try:
            plug_board = PlugBoard(["aba", "ab"])
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('Plugboard__init__: pairs length must be 2')))

    def test_plug_board_2(self):
        try:
            plug_board = PlugBoard(["ab", "cd", "be"])
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('Plugboard__init__: dual uses of characters')))

    def test_plug_board_3(self):
        try:
            plug_board = PlugBoard(["ab", "cd", "be"])
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('Plugboard__init__: dual uses of characters')))

    def test_plug_board_4(self):
        try:
            plug_board = PlugBoard(["a!"])
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('EnigmaStatic_valid_character: unexpected character, enigma only supports A-Z characters')))

    def test_plug_board_5(self):
        paris = ["ab", "cd"]
        plug_board = PlugBoard(paris)
        for pair in paris:
            pair = pair.upper()
            (i, j) = (pair[0], pair[1])
            self.assertEqual(i, plug_board.get_plug_char(j))
            self.assertEqual(j, plug_board.get_plug_char(i))

    def test_reflector_1(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['A'])
        self.assertEqual(reflector.rotor_description, EnigmaSettings.get_reflectors()['A'])

    def test_reflector_2(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['A'])
        self.assertEqual(reflector.wiring, dict({1: 5, 2: 10, 3: 13, 4: 26, 5: 1, 6: 12, 7: 25, 8: 24, 9: 22, 10: 2, 11: 23, 12: 6, 13: 3, 14: 18, 15: 17, 16: 21, 17: 15, 18: 14, 19: 20, 20: 19, 21: 16, 22: 9, 23: 11, 24: 8, 25: 7, 26: 4}))

    def test_reflector_3(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['A'])
        self.assertEqual(reflector.wiring_back, dict({5: 1, 10: 2, 13: 3, 26: 4, 1: 5, 12: 6, 25: 7, 24: 8, 22: 9, 2: 10, 23: 11, 6: 12, 3: 13, 18: 14, 17: 15, 21: 16, 15: 17, 14: 18, 20: 19, 19: 20, 16: 21, 9: 22, 11: 23, 8: 24, 7: 25, 4: 26}))

    def test_reflector_4(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['A'])
        reflector.set_position('D')
        self.assertEqual(reflector.pins_to_ring_settings, dict({1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 13, 11: 14, 12: 15, 13: 16, 14: 17, 15: 18, 16: 19, 17: 20, 18: 21, 19: 22, 20: 23, 21: 24, 22: 25, 23: 26, 24: 1, 25: 2, 26: 3}))

    def test_reflector_5(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['A'])
        reflector.set_position('D')
        self.assertEqual(reflector.ring_settings_to_keys, dict({4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, 12: 9, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 17, 21: 18, 22: 19, 23: 20, 24: 21, 25: 22, 26: 23, 1: 24, 2: 25, 3: 26}))

    def test_rotor_1(self):
        rotor = Rotor(EnigmaSettings.get_rotors()['I'])
        self.assertEqual(rotor.rotor_description, EnigmaSettings.get_rotors()['I'])

    def test_rotor_2(self):
        rotor = Rotor(EnigmaSettings.get_rotors()['I'])
        end_char = ord(EnigmaSettings.get_rotors()['I']['notch']) - ord('A')
        rotor.set_position('A')
        for i in range(0, end_char - 1):
            self.assertEqual(False, rotor.click())
        self.assertEqual(True, rotor.click())

    def test_rotor_mechanism_1(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['B']) #A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A') #I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], None)
        try:
            rotor_mechanism.process(25)
            self.assertFalse(True)
        except AttributeError as ae:
            self.assertEqual(str(ae), str(AttributeError('\'NoneType\' object has no attribute \'wiring\'')))
        try:
            rotor_mechanism.process(225)
            self.assertFalse(True)
        except KeyError as ke:
            self.assertFalse(False)

    def test_rotor_mechanism_2(self):
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A') #I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], None)
        try:
            rotor_mechanism.process(25)
            self.assertFalse(True)
        except AttributeError as ae:
            self.assertEqual(str(ae), str(AttributeError('\'NoneType\' object has no attribute \'wiring\'')))
        try:
            rotor_mechanism.process(225)
            self.assertFalse(True)
        except KeyError as ke:
            self.assertTrue(True)

    def test_rotor_mechanism_3(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        self.assertEqual('B', chr(rotor_mechanism.process(ord('A') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('D', chr(rotor_mechanism.process(ord('A') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('Z', chr(rotor_mechanism.process(ord('A') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('G', chr(rotor_mechanism.process(ord('A') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('O', chr(rotor_mechanism.process(ord('A') - ord('A') + 1) - 1 + ord('A')))

    def test_rotor_mechanism_4(self):
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        self.assertEqual('A', chr(rotor_mechanism.process(ord('B') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('A', chr(rotor_mechanism.process(ord('D') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('A', chr(rotor_mechanism.process(ord('Z') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('A', chr(rotor_mechanism.process(ord('G') - ord('A') + 1) - 1 + ord('A')))
        self.assertEqual('A', chr(rotor_mechanism.process(ord('O') - ord('A') + 1) - 1 + ord('A')))

    def test_enigma_1(self):
        plug_board = PlugBoard([])
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        enigma_key = Key()
        enigma_key.set_key('I', 'D')
        enigma_key.set_key('II', 'O')
        enigma_key.set_key('III', 'G')
        enigma = Enigma(enigma_key, plug_board, rotor_mechanism)
        p_text = "ENIGMA"
        c_text = enigma.encryption(p_text)
        p_text_2 = enigma.decryption(c_text)
        print('')
        print(c_text)
        print('')
        self.assertEqual(p_text, p_text_2)

    def test_enigma_2(self):
        plug_board = PlugBoard(['ab', 'ce'])
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        enigma_key = Key()
        enigma_key.set_key('I', 'D')
        enigma_key.set_key('II', 'O')
        enigma_key.set_key('III', 'G')
        enigma = Enigma(enigma_key, plug_board, rotor_mechanism)
        p_text = "ENIGMA"
        c_text = enigma.encryption(p_text)
        p_text_2 = enigma.decryption(c_text)
        self.assertEqual(p_text, p_text_2)

    def test_enigma_3(self):
        plug_board = PlugBoard(['ab', 'ce'])
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        enigma_key = Key()
        enigma_key.set_key('I', 'D')
        enigma_key.set_key('II', 'O')
        enigma_key.set_key('III', 'G')
        enigma = Enigma(enigma_key, plug_board, rotor_mechanism)
        p_text = "3"
        try:
            c_text = enigma.encryption(p_text)
            self.assertFalse(True)
        except ValueError as ve:
            self.assertEqual(str(ve), str(ValueError('EnigmaStatic_valid_character: unexpected character, enigma only supports A-Z characters')))

    def test_cbc_mode_1(self):
        pain_text = 'ABC'
        plug_board = PlugBoard(['ab', 'ce'])
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['I'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        cbc_key = Key[str]()
        cbc_key.set_key('cbc_key', '234ASD ADSD')
        enigma_key = Key()
        enigma_key.set_key('I', 'D')
        enigma_key.set_key('II', 'O')
        enigma_key.set_key('III', 'G')
        enigma = Enigma(enigma_key, plug_board, rotor_mechanism)
        cbc_mode = InverseCBCMode(enigma, cbc_key)
        c_msg = cbc_mode.encryption(pain_text)
        p_msg = cbc_mode.decryption(c_msg)
        pain_text += (len(p_msg) - len(pain_text)) * 'F'
        self.assertEqual(pain_text, p_msg)

    def test_cbc_mode_2(self):
        pain_text = 'ABC'
        plug_board = PlugBoard(['ab', 'ce'])
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        enigma_key = Key[str]()
        enigma_key.set_key('I', 'D')
        enigma_key.set_key('II', 'O')
        enigma_key.set_key('III', 'G')
        enigma = Enigma(enigma_key, plug_board, rotor_mechanism)
        cbc_key = Key[str]()
        cbc_key.set_key('cbc_key', '230000000SD')
        cbc_mode = InverseCBCMode(enigma, cbc_key)
        c_msg = cbc_mode.encryption(pain_text)
        p_msg = cbc_mode.decryption(c_msg)
        pain_text += (len(p_msg) - len(pain_text)) * 'F'
        self.assertEqual(pain_text, p_msg)

    def test_cbc_mode_3(self):
        pain_text = 'ABCC'
        plug_board = PlugBoard(['ab', 'ce'])
        reflector = Reflector(EnigmaSettings.get_reflectors()['B'])  # A/B/C
        rotor_1 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_2 = Rotor(EnigmaSettings.get_rotors()['II'], 'A')  # I / II / III / IV / V
        rotor_3 = Rotor(EnigmaSettings.get_rotors()['III'], 'A')  # I / II / III / IV / V
        rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
        enigma_key = Key[str]()
        enigma_key.set_key('I', 'D')
        enigma_key.set_key('II', 'O')
        enigma_key.set_key('III', 'G')
        enigma = Enigma(enigma_key, plug_board, rotor_mechanism)
        cbc_key = Key[str]()
        cbc_key.set_key('cbc_key', '0SD')
        cbc_mode = InverseCBCMode(enigma, cbc_key)
        c_msg = cbc_mode.encryption(pain_text)
        p_msg = cbc_mode.decryption(c_msg)
        pain_text += (len(p_msg) - len(pain_text)) * 'F'
        self.assertEqual(pain_text, p_msg)

if __name__ == '__main__':
    unittest.main()
