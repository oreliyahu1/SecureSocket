from SecureSocket.ISecureSocket import ISecureSocket
from ICrypto.IKeyExchangeGenerator import IKeyExchangeGenerator
import socket
import json


class SecureServer(ISecureSocket):

    def __init__(self, crypto_settings: dict, crypto_maker, ip_address, port, max_recv_buffer=4096, end_flag='0x0x[END]x0x0', max_queue_requests=1):
        super().__init__(crypto_maker, ip_address, port, max_recv_buffer, end_flag)
        self.max_queue_requests = max_queue_requests
        self.crypto_settings = crypto_settings

    def start(self):
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(self.max_queue_requests)

    def secure_start(self):
        self.start()

    def get_new_connection(self) -> (socket, any):
        return self.socket.accept()

    def secure_get_new_connection(self) -> (socket, any):
        (socket, any) = self.get_new_connection()

        ke_settings, key_exchange = self.create_key_exchange_generator(self.crypto_settings)
        self.send_to_socket(socket, str(ke_settings))
        if key_exchange is not None:
            recv_message = self.recv_from_socket(socket)
            ke_settings: dict = json.loads(recv_message.pop(0).replace("'", "\""))
            self.create_key_exchange_generator_2nd(key_exchange, ke_settings)

        d_settings, app_message = self.create_app_message_generator(self.crypto_settings)
        self.app_message[str(socket.getpeername())] = app_message

        if key_exchange is not None:
            self.send_to_socket(socket, str(key_exchange.generate_message(str(d_settings))))
            recv_message = self.recv_from_socket(socket)
            c_settings: dict = json.loads(recv_message.pop(0).replace("'", "\""))
            c_settings: dict = json.loads(key_exchange.degenerate_message(c_settings).replace("'", "\""))
        else:
            self.send_to_socket(socket, str(d_settings))
            recv_message = self.recv_from_socket(socket)
            c_settings: dict = json.loads(recv_message.pop(0).replace("'", "\""))

        self.create_app_message_generator_2nd(app_message, c_settings)
        return (socket, any)
