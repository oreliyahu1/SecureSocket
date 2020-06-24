import abc
import socket
from Socket.ISocket import ISocket
from ICrypto.ICryptoMessageGenerator import ICryptoMessageGenerator
from ICrypto.IKeyExchangeGenerator import IKeyExchangeGenerator
from ICrypto.ICryptoMaker import ICryptoMaker
from typing import Dict


class ISecureSocket(ISocket):

    def __init__(self, crypto_maker: ICryptoMaker, ip_address, port, max_recv_buffer=4096, end_flag='0x0x[END]x0x0'):
        super().__init__(ip_address, port, max_recv_buffer, end_flag)
        self.app_message: Dict[ICryptoMessageGenerator] = dict()
        self.crypto_maker = crypto_maker
        if self.crypto_maker is None:
            raise ValueError('ISecureSocket: __init__ crypto_maker cannot be None')

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError('ISecureSocket: start function is not defined')

    @abc.abstractmethod
    def secure_start(self):
        raise NotImplementedError('ISecureSocket: secure_start function is not defined')

    def secure_recv_from_socket(self, c_socket: socket) -> list:
        pain_texts = []
        msgs = self.recv_from_socket(c_socket)
        for msg in msgs:
            pain_texts.append(self.app_message[str(c_socket.getpeername())].degenerate_message(self.crypto_maker.get_crypto_message(msg)))
        return pain_texts

    def secure_send_to_socket(self, c_socket: socket, data: str):
        self.send_to_socket(c_socket, self.app_message[str(c_socket.getpeername())].generate_message(data).get_dict_message())

    def create_app_message_generator(self, crypto_settings: dict) -> (dict, ICryptoMessageGenerator):
        (sc, crypto) = self.crypto_maker.get_crypto(crypto_settings.get('crypto'), crypto_settings)
        (bc, block_cipher_mode) = self.crypto_maker.get_block_cipher_mode(crypto_settings.get('block_mode'), crypto_settings, crypto)
        (dc, digital_signature) = self.crypto_maker.get_signature(crypto_settings.get('digital_signature'), crypto_settings, False)

        if crypto is None:
            raise NotImplementedError("SecureServer: secure_get_new_connection crypto cannot be None")
        if block_cipher_mode:
            crypto = block_cipher_mode

        return {**sc, **bc, **dc, 'crypto': crypto_settings.get('crypto'), 'block_mode': crypto_settings.get('block_mode'), 'digital_signature': crypto_settings.get('digital_signature')},\
               self.crypto_maker.get_app_message_generator(crypto, digital_signature)

    def create_app_message_generator_2nd(self, app_message: ICryptoMessageGenerator, crypto_settings: dict):
        (dc, digital_signature) = self.crypto_maker.get_signature(crypto_settings.get('digital_signature'), crypto_settings, True)
        app_message.set_public_signature(digital_signature)

    def create_key_exchange_generator(self, crypto_settings: dict) -> (dict, IKeyExchangeGenerator):
        if not crypto_settings.get('key_exchange') or len(crypto_settings.get('key_exchange')) == 0:
            return None, None
        (kec, key_exchange) = self.crypto_maker.get_key_exchange(crypto_settings.get('key_exchange'), crypto_settings, False, None)
        return {**kec, 'key_exchange': crypto_settings.get('key_exchange')}, self.crypto_maker.get_key_exchange_generator(None, key_exchange)

    def create_key_exchange_generator_2nd(self, key_exchange: IKeyExchangeGenerator, crypto_settings: dict):
        self.crypto_maker.get_key_exchange(crypto_settings.get('key_exchange'), crypto_settings, True, key_exchange)
        self.crypto_maker.get_crypto(crypto_settings.get(crypto_settings.get('key_exchange')['type']).get('crypto'),
                                                    crypto_settings.get(crypto_settings.get('key_exchange')['type']), key_exchange)

