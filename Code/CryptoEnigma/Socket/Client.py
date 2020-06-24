from Socket.ISocket import ISocket


class Client(ISocket):

    def start(self):
        self.socket.connect((self.ip_address, self.port))

    def send(self, data: str):
        super().send_to_socket(self.socket, data)

    def recv(self) -> list:
        return self.recv_from_socket(self.socket)