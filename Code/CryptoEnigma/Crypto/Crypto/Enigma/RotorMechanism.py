from typing import List
from Crypto.Crypto.Enigma.Reflector import Reflector
from Crypto.Crypto.Enigma.Rotor import Rotor


class RotorMechanism(object):

    def __init__(self, list_rotors: List[Rotor], reflector: Reflector):
        self.rotors = list_rotors
        self.reflector = reflector

    def set_rotor_position(self, rotor_slot: int, position: chr):
        self.rotors[rotor_slot].set_position(position)

    def set_reflector(self, reflector: Reflector):
        self.reflector = reflector

    def process(self, bit_in: int) -> int:
        next_bit = bit_in

        for rotor in self.rotors:
            if not rotor.click():
                break

        for rotor in self.rotors:
            entry_face, exit_face = rotor.get_faces()
            entry_pin = entry_face[next_bit]
            exit_pin = rotor.wiring[entry_pin]
            next_bit = exit_face[exit_pin]
        next_bit = self.reflector.wiring[next_bit]
        for rotor in reversed(self.rotors):
            entry_face, exit_face = rotor.get_faces()
            entry_pin = entry_face[next_bit]
            exit_pin = rotor.wiring_back[entry_pin]
            next_bit = exit_face[exit_pin]
        return next_bit

    def copy(self):
        rotors_copy = []
        for rotor in self.rotors:
            rotors_copy.append(rotor.copy())
        reflector_copy = self.reflector.copy()
        return RotorMechanism(rotors_copy, reflector_copy)