from Crypto.Crypto.Enigma.EnigmaStatic import az_to_index


class Reflector(object):

    def __init__(self, rotor_description, ring_settings: chr = 'A'):
        self.rotor_description = rotor_description.copy()
        self.position = 0
        self.ring_settings_to_keys: dict = {}
        self.pins_to_ring_settings: dict = {}
        self.set_position(ring_settings)

        self.wiring = {}
        self.wiring_back = {}
        for shifted_input in self.ring_settings_to_keys:
            in_pin = self.ring_settings_to_keys[shifted_input]
            out_pin = self.pins_to_ring_settings[rotor_description.get('wiring')[str(in_pin)]]
            self.wiring.update({shifted_input: out_pin})
            self.wiring_back.update({out_pin: shifted_input})

    def set_position(self, char: chr):
        self.position = az_to_index(char)
        self.ring_settings_to_keys: dict = {}
        self.pins_to_ring_settings: dict = {}
        pos = self.position
        for i in range(0, 26):
            pos = pos % 26
            self.ring_settings_to_keys.update({pos + 1: i + 1})
            self.pins_to_ring_settings.update({i + 1: pos + 1})
            pos += 1

    def copy(self):
        reflector_copy = Reflector(self.rotor_description)
        reflector_copy.position = self.position
        reflector_copy.ring_settings_to_keys = self.ring_settings_to_keys.copy()
        reflector_copy.pins_to_ring_settings = self.pins_to_ring_settings.copy()
        reflector_copy.wiring = self.wiring.copy()
        reflector_copy.wiring_back = self.wiring_back.copy()
        return reflector_copy
