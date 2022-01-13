from ICrypto.ICrypto import ICrypto
from Crypto.Crypto.Enigma.EnigmaStatic import valid_character, az_to_index, index_to_az
from Crypto.Crypto.Enigma.PlugBoard import PlugBoard
from Crypto.Crypto.Enigma.RotorMechanism import RotorMechanism
from ICrypto.IKey import IKey


class Enigma(ICrypto[str, str]):

    def __init__(self, key: IKey[str], plug_board: PlugBoard, rotor_mechanism: RotorMechanism):
        self.key = key
        self.plug_board = plug_board
        self.rotor_mechanism_encryption = rotor_mechanism
        self.rotor_mechanism_decryption = rotor_mechanism
        self.set_rotor_mechanism(rotor_mechanism)

    def set_key(self, key: IKey):
        if key is None or key.size() != len(self.rotor_mechanism_encryption.rotors):
            raise ValueError('Enigma_set_key: key length must be equal to the number of rotors')
        key_setting = []
        for char in key.get_keys_name():
            valid_character(key.get_key(char), True)
            key_setting.append(key.get_key(char.upper()))
        self.key = ''.join(key_setting)
        key_setting.reverse()
        for i, c in enumerate(key_setting):
            self.rotor_mechanism_encryption.set_rotor_position(i, c)
        self.rotor_mechanism_decryption = self.rotor_mechanism_encryption.copy()

    def write_text(self, text: str, rotor_mechanism: RotorMechanism) -> str:
        if text is None: text = ''
        after_text = ''
        text = text.upper()
        for character in text: valid_character(character, True)

        for character in text:
            if self.plug_board is not None:
                plug_board_character = self.plug_board.get_plug_char(character)
            else:
                plug_board_character = character
            plug_board_num = az_to_index(plug_board_character) + 1
            wheel_pack_num = rotor_mechanism.process(plug_board_num)
            wheel_pack_character = index_to_az(wheel_pack_num - 1)
            if self.plug_board is not None:
                plug_board_character_2 = self.plug_board.get_plug_char(wheel_pack_character)
            else:
                plug_board_character_2 = wheel_pack_character
            after_text += plug_board_character_2

        return after_text

    def encryption(self, pain_text: str) -> str:
        return self.write_text(pain_text, self.rotor_mechanism_encryption)

    def decryption(self, cipher_text: str) -> str:
        return self.write_text(cipher_text, self.rotor_mechanism_decryption)

    def set_plug_board(self, plug_board: PlugBoard):
        self.plug_board = plug_board

    def set_rotor_mechanism(self, rotor_mechanism: RotorMechanism):
        self.rotor_mechanism_encryption = rotor_mechanism
        self.rotor_mechanism_decryption = rotor_mechanism.copy()
        if self.key.size() != len(self.rotor_mechanism_encryption.rotors):
            raise ValueError('Enigma_set_key: number of rotors must be equal to key length')
        self.set_key(self.key)
