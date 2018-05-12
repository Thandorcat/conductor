import socket
import psutil as psutil


class Metric:
    def __init__(self, port, ip=None):
        self.ip = ip
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = 'listen_port'

    def check(self):
        if self.ip:
            for connection in psutil.net_connections():
                if connection.laddr.port == self.port \
                        and connection.laddr.ip == self.ip \
                        and connection.status == 'LISTEN':
                    return True
            return False
        else:
            result = self.socket.connect_ex(('127.0.0.1', self.port))
            if result == 0:
                return True
            else:
                return False


