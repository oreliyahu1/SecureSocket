from Socket.ISocket import ISocket
import socket


class Server(ISocket):

    def __init__(self, ip_address, port, max_recv_buffer=4096, end_flag='0x0x[END]x0x0', max_queue_requests=1):
        super().__init__(ip_address, port, max_recv_buffer, end_flag)
        self.max_queue_requests = max_queue_requests

    def start(self):
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(self.max_queue_requests)

    def get_new_connection(self) -> (socket, any):
        return self.socket.accept()
