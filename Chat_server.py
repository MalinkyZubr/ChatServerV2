import socket
import asyncio
import threading
import ssl
from ssl import SSLContext
import json


class User:
    def __init__(self, connection=None, ip_port=None, username=None, SSLkey=None):
        self.connection = connection
        self.ip, self.port = ip_port
        self.username = username
        self.ssl_key = SSLkey
    
    def receive_and_unpack(self):
        json_package = ""
        while True:
            try:
                json_package = json_package + \
                    self.connection.recv(32768).decode('utf-8')
                return json.loads(json_package)
            except ValueError:
                continue

    def pack_and_send(self, data):
        json_package = json.dumps(data)
        self.connection.send(json_package.encode('utf-8'))


class Server:
    def __init__(self, IP, PORT):
        sys_log_file = filename = os.path.join(pwd, r'system_logs.txt')
        msg_log_file = filename = os.path.join(pwd, r'message_logs.txt')

        self.IP = IP
        self.PORT = PORT
        self.connections = []
        self.message_queue = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.IP, self.PORT))
        self.sock.listen(50)

        self.connections_lock = Lock()
        self.message_lock = Lock()

        self.socket_opts = SocketOpts()
    
    async def accept_users(self): 
        connection, ip_port = self.sock.accept()
        user = User(connection=connection, ip_port=ip_port)
        SSL_key = user.receive_and_unpack()['Key']
        user.ssl_key = SSL_key
        

    async def receive(self, connection):
        
