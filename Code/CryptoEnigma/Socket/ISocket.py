import socket
import abc


class ISocket(object, metaclass=abc.ABCMeta):

    def __init__(self, ip_address, port, max_recv_buffer=4096, end_flag='0x0x[END]x0x0'):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = ip_address
        self.port = port
        self.max_recv_buffer = max_recv_buffer
        self.end_flag = end_flag

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError('ISocket: start function is not defined')

    def recv_from_socket(self, c_socket: socket) -> list:
        list_recv_data = list()
        recv_data = ''
        while True:
            data = c_socket.recv(self.max_recv_buffer)
            recv_data += data.decode('utf-8')
            end_index = recv_data.find(self.end_flag)
            if end_index != -1:
                datas = recv_data.split(self.end_flag)
                list_recv_data += datas
                recv_data = list_recv_data.pop(-1)
                if not datas[-1]:
                    break

        return list(filter(lambda x: x != '', list_recv_data))

    def send_to_socket(self, c_socket: socket, data: str):
        c_socket.send(bytes(self.end_flag + str(data) + self.end_flag, 'utf-8'))

    def close(self):
        return self.socket.close()