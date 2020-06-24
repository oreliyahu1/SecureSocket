from Crypto.Crypto.Enigma.Reflector import Reflector
from Crypto.Crypto.Enigma.EnigmaStatic import az_to_index


class Rotor(Reflector):

    def __init__(self, rotor_description: dict, ring_settings: chr = 'A'):
        super().__init__(rotor_description, ring_settings)
        self.end_char_index = az_to_index(rotor_description.get('notch'))

    def click(self) -> bool:
        self.position = (self.position + 1) % 26
        self.set_position(chr(ord('A') + self.position))
        if self.position == self.end_char_index:
            return True
        return False

    def get_faces(self) -> (dict, dict):
        return self.pins_to_ring_settings, self.ring_settings_to_keys

    def copy(self):
        rotor_copy = Rotor(self.rotor_description)
        rotor_copy.position = self.position
        rotor_copy.ring_settings_to_keys = self.ring_settings_to_keys.copy()
        rotor_copy.pins_to_ring_settings = self.pins_to_ring_settings.copy()
        rotor_copy.wiring = self.wiring.copy()
        rotor_copy.wiring_back = self.wiring_back.copy()
        rotor_copy.end_char_index = self.end_char_index
        return rotor_copy
