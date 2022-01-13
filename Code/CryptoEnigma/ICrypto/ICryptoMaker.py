import abc
from typing import Dict

from ICrypto.ICryptoMessage import ICryptoMessage
from ICrypto.ICryptoMessageGenerator import ICryptoMessageGenerator
from ICrypto.IKeyExchangeGenerator import IKeyExchangeGenerator
from ICrypto.ICrypto import ICrypto
from ICrypto.ICryptoWMode import ICryptoWMode
from ICrypto.ISignature import ISignature
from ICrypto.IKeyExchange import IKeyExchange


class ICryptoMaker(object, metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_app_message_generator(*args) -> ICryptoMessageGenerator:
        raise NotImplementedError('ICryptoMaker: get_app_message_generator function is not defined')

    @staticmethod
    @abc.abstractmethod
    def get_key_exchange_generator(*args) -> IKeyExchangeGenerator:
        raise NotImplementedError('ICryptoMaker: get_key_exchange_generator function is not defined')

    @staticmethod
    @abc.abstractmethod
    def get_crypto_message(*args) -> ICryptoMessage:
        raise NotImplementedError('ICryptoMaker: get_crypto_message function is not defined')

    @staticmethod
    @abc.abstractmethod
    def get_crypto(type: dict, settings: dict, *args) -> (Dict[str, dict], ICrypto):
        raise NotImplementedError('ICryptoMaker: get_crypto function is not defined')

    @staticmethod
    @abc.abstractmethod
    def get_block_cipher_mode(type: dict, settings: dict, *args) -> (Dict[str, dict], ICryptoWMode):
        raise NotImplementedError('ICryptoMaker: get_block_cipher_mode function is not defined')

    @staticmethod
    def get_key_exchange(type: dict, settings: dict, *args) -> (Dict[str, dict], IKeyExchange):
        raise NotImplementedError('ICryptoMaker: get_key_exchange function is not defined')

    @staticmethod
    @abc.abstractmethod
    def get_signature(type: dict, settings: dict, *args) -> (Dict[str, dict], ISignature):
        raise NotImplementedError('ICryptoMaker: get_signature function is not defined')
