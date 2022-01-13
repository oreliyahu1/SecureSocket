from SecureSocket.ISecureSocket import ISecureSocket
import json


class SecureClient(ISecureSocket):

    def start(self):
        self.socket.connect((self.ip_address, self.port))

    def secure_start(self):
        self.start()
        key_exchange = None
        recv_message = self.recv()
        ke_settings = recv_message.pop(0)

        if ke_settings != 'None':
            ke_settings: dict = json.loads(ke_settings.replace("'", "\""))
            cke_settings, key_exchange = self.create_key_exchange_generator(ke_settings)
            if key_exchange:
                self.create_key_exchange_generator_2nd(key_exchange, ke_settings)
                self.send(cke_settings)

        recv_message = self.recv()
        crypto_settings: dict = json.loads(recv_message.pop(0).replace("'", "\""))
        if key_exchange is not None:
            crypto_settings: dict = json.loads(key_exchange.degenerate_message(crypto_settings).replace("'", "\""))
            d_settings, app_message = self.create_app_message_generator(crypto_settings)
            self.create_app_message_generator_2nd(app_message, crypto_settings)
            self.app_message[str(self.socket.getpeername())] = app_message
            self.send(str(key_exchange.generate_message(str(d_settings))))
        else:
            d_settings, app_message = self.create_app_message_generator(crypto_settings)
            self.create_app_message_generator_2nd(app_message, crypto_settings)
            self.app_message[str(self.socket.getpeername())] = app_message
            self.send(d_settings)


    def send(self, data: str):
        super().send_to_socket(self.socket, data)

    def recv(self) -> list:
        return self.recv_from_socket(self.socket)

    def secure_send(self, data: str):
        super().secure_send_to_socket(self.socket, data)

    def secure_recv(self) -> list:
        return self.secure_recv_from_socket(self.socket)