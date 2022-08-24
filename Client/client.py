import json
import socket
import sys

sys.path.insert(0, r'New-chat-server\encryption-algorithms')
from SSL import SSLSystem
from AES import AESSystem
sys.path.insert(1, r'New-chat-server\classes')
from User import userClientSide

# 
    # class User:
    #     def __init__(self, connection=None, ip_port=None, username=None, password=None):
    #         self.connection = connection

    #         self.username = username
    #         self.password = password
    #         self.ip, self.port = ip_port

    #         self.ssl_system = SSLSystem()
    #         self.aes_system = None

    #     def receive_and_unpack(self, encrypted=False):
    #         json_package = ""
    #         while True:
    #             if not encrypted:
    #                 try:
    #                     json_package = json_package + \
    #                         self.connection.recv(32768).decode('utf-8')
    #                     return json.loads(json_package)
    #                 except ValueError:
    #                     continue
    #             else:
    #                 try:
    #                     json_package = json_package + \
    #                         self.aes_system.decrypt(self.connection.recv(32768).decode('utf-8'))
    #                     return json.loads(json_package)
    #                 except ValueError:
    #                     continue

    #     def pack_and_send(self, data, encrypted=False):
    #         if not encrypted:
    #             json_package = json.dumps(data)
    #             self.connection.send(json_package.encode('utf-8'))
    #         else:
    #             json_package = json.dumps(data)
    #             json_package = self.aes_system.encrypt(json_package)
    #             self.connection.send(json_package)

    #     def key_exchange(self):
    #         public_key = self.receive_and_unpack()
    #         aes_key, encrypted_aes = self.ssl_system.generate_message(public_key)
    #         self.aes_system = AESSystem(int(aes_key))
    #         self.pack_and_send(encrypted_aes)

    #     def connect(self, t='login'):
    #         self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.connection.connect((self.ip, self.port))
    #         self.key_exchange()
    #         request = {'request_type':t, 'username':self.username, 'password':self.password}
    #         self.pack_and_send(request, encrypted=True)
    #         response = self.receive_and_unpack(encrypted=True)

    #         if response['response'] == 'Connection failed':
    #             print('Connection failed')

class Client:
    def __init__(self, IP, PORT, username, password, request_type='login'):
        self.user = userClientSide(ip_port=(IP, PORT), username=username, password=password)
        self.user.connect(t=request_type)
        self.user.pack_and_send('Hello')

if __name__ == "__main__":
    client = Client('192.168.0.173', 4444, 'sugma', 'TEST')





