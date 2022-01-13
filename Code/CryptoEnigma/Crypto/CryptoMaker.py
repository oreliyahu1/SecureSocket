import json
import copy
from typing import Dict, List

from ICrypto.ICryptoMessageGenerator import ICryptoMessageGenerator
from ICrypto.IKeyExchangeGenerator import IKeyExchangeGenerator
from ICrypto.ICryptoMaker import ICryptoMaker
from ICrypto.ICryptoMessage import ICryptoMessage
from ICrypto.ICrypto import ICrypto
from ICrypto.ICryptoWMode import ICryptoWMode
from ICrypto.ISignature import ISignature
from ICrypto.IKeyExchange import IKeyExchange

from Crypto.Generator.AppMessageGenerator import AppMessageGenerator
from Crypto.Generator.KeyExchangeGenerator import KeyExchangeGenerator
from Crypto.CryptoMessage import CryptoMessage
from Crypto.Key import Key

from Crypto.Crypto.Enigma.EnigmaSettings import EnigmaSettings
from Crypto.Crypto.Enigma.PlugBoard import PlugBoard
from Crypto.Crypto.Enigma.Reflector import Reflector
from Crypto.Crypto.Enigma.Rotor import Rotor
from Crypto.Crypto.Enigma.RotorMechanism import RotorMechanism
from Crypto.Crypto.Enigma.Enigma import Enigma
from Crypto.BlockCipherMode.InverseCBCMode import InverseCBCMode
from Crypto.DigitalSignature.ElGamalDigitalSignature import ElGamalDigitalSignature

from Crypto.Crypto.Caesar.Caesar import Caesar

from Crypto.KeyExchange.DiffieHellman import DiffieHellman


class CryptoMaker(ICryptoMaker):

    @staticmethod
    def get_app_message_generator(*args) -> ICryptoMessageGenerator:
        return AppMessageGenerator(*args)

    @staticmethod
    def get_key_exchange_generator(*args) -> IKeyExchangeGenerator[str, List[int]]:
        return KeyExchangeGenerator[str, List[int]](*args)

    @staticmethod
    def get_crypto_message(*args) -> ICryptoMessage:
        c_msg: dict = json.loads(args[0].replace("'", "\""))
        return CryptoMessage(c_msg.get('message'), c_msg.get('signature'))

    @staticmethod
    def get_crypto(type: dict, settings: dict, *args) -> (Dict[str, dict], ICrypto):
        type = CryptoMaker.get_type(type)

        if type == 'enigma':
            settings = CryptoMaker.get_settings(type, settings)
            enigma_str_key, enigma_reflector, enigma_rotors, enigma_plugboard = settings['key'], settings['reflector'], settings['rotors'], settings['plug_board']

            plug_board = PlugBoard(enigma_plugboard)
            reflector = Reflector(EnigmaSettings.get_reflectors()[enigma_reflector])  # A/B/C
            rotor_1 = Rotor(EnigmaSettings.get_rotors()[enigma_rotors['1']['type']],
                            enigma_rotors['1']['ring'])  # I / II / III / IV / V
            rotor_2 = Rotor(EnigmaSettings.get_rotors()[enigma_rotors['2']['type']],
                            enigma_rotors['2']['ring'])  # I / II / III / IV / V
            rotor_3 = Rotor(EnigmaSettings.get_rotors()[enigma_rotors['3']['type']],
                            enigma_rotors['3']['ring'])  # I / II / III / IV / V

            enigma_key = Key[str]()
            for i, char in enumerate(enigma_str_key):
                enigma_key.set_key(str(i), char)
            rotor_mechanism = RotorMechanism([rotor_3, rotor_2, rotor_1], reflector)
            return {type: dict(settings)}, Enigma(enigma_key, plug_board, rotor_mechanism)
        elif type == 'caesar':
            key_exchange: IKeyExchangeGenerator = args[0]
            caesar_key = Key[int]({'key': key_exchange.get_key_exchange().get_k()})
            key_exchange.set_crypto(Caesar(caesar_key))
        else:
            return None

    @staticmethod
    def get_block_cipher_mode(type: dict, settings: dict, *args) -> (Dict[str, dict], ICryptoWMode):
        type = CryptoMaker.get_type(type)

        if type == 'cbc':
            settings = CryptoMaker.get_settings(type, settings)
            crypto_mode_key = settings['key']
            cbc_key = Key[str]()
            cbc_key.set_key('cbc_key', crypto_mode_key)
            return {type: dict(settings)}, InverseCBCMode(args[0], cbc_key)
        else:
            return None

    @staticmethod
    def get_signature(type: dict, settings: dict, *args) -> (Dict[str, dict], ISignature):
        type = CryptoMaker.get_type(type)

        if type == 'el_gamal':
            settings = CryptoMaker.get_settings(type, settings)
            el_gamal_hash_function = settings['hash_function']
            if not args[0]:
                settings_wp = dict(settings)
                el_gamal = ElGamalDigitalSignature(el_gamal_hash_function)
                settings_wp['2nd_stage'] = dict()
                settings_wp.get('2nd_stage')['public_signature_keys'] = el_gamal.get_public_keys().keys
                return {type: settings_wp}, el_gamal
            else:
                el_gamal_public_keys = Key[int](settings.get('2nd_stage')['public_signature_keys'])
                return {type: dict(settings)}, ElGamalDigitalSignature(el_gamal_hash_function, el_gamal_public_keys)
        else:
            return None

    @staticmethod
    def get_key_exchange(type: dict, settings: dict, *args) -> (Dict[str, dict], IKeyExchange):
        type = CryptoMaker.get_type(type)

        if type == 'diffiehellman':
            settings = CryptoMaker.get_settings(type, settings)
            settings_wp = copy.deepcopy(settings)
            if not args[0]:
                if settings.get('2nd_stage') is None:
                    diffie_hellman = DiffieHellman()
                    settings_wp['2nd_stage'] = dict()
                    settings_wp.get('2nd_stage')['keys'] = diffie_hellman.get_key()
                    return {type: settings_wp}, diffie_hellman
                else:
                    ex_keys = Key[int](settings.get('2nd_stage')['keys'])
                    diffie_hellman = DiffieHellman(ex_keys)
                    settings_wp.get('2nd_stage')['keys'] = diffie_hellman.get_key()
                    return {type: dict(settings_wp)}, diffie_hellman
            else:
                ex_keys = Key[int](settings.get('2nd_stage')['keys'])
                key_exchange: IKeyExchangeGenerator = args[1]
                key_exchange.get_key_exchange().set_key(ex_keys)
        else:
            return None

    @staticmethod
    def get_type(type: dict) -> str:
        if type.get('type') is None:
            raise ValueError('CryptoMaker: get_type type cannot be None')
        return type.get('type')

    @staticmethod
    def get_settings(type: str, settings: dict) -> dict:
        if settings.get(type) is None:
            raise ValueError('CryptoMaker: get_type settings must include type')
        return settings.get(type)