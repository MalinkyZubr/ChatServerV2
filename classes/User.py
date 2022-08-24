import socket
from SSL import SSLSystem
from AES import AESSystem
import json
import asyncio


class User:
    def __init__(self, connection=None, ip_port=None):
        self.connection = connection
        self.ip, self.port = ip_port
        self.username = None
        self.ssl_system = SSLSystem()
        self.aes_system = None

    def receive_and_unpack(self, encrypted=False):
        json_package = ""
        while True:
            if not encrypted:
                try:
                    json_package = json_package + \
                        self.connection.recv(32768).decode('utf-8')
                    return json.loads(json_package)
                except ValueError:
                    continue
            else:
                try:
                    json_package = json_package + \
                        self.aes_system.decrypt(self.connection.recv(32768).decode('utf-8'))
                    return json.loads(json_package)
                except ValueError:
                    continue

    def pack_and_send(self, data, encrypted=False):
        if not encrypted:
            json_package = json.dumps(data)
            self.connection.send(json_package.encode('utf-8'))
        else:
            json_package = json.dumps(data)
            json_package = self.aes_system.encrypt(json_package)
            self.connection.send(json_package)


class userServerSide(User):
    def __init__(self, connection=None, ip_port=None):
        super().__init__(connection, ip_port)

    def key_exchange(self):
        private_key, public_key = self.ssl_system.create_keys()
        print(public_key)
        self.pack_and_send(public_key)
        cipher_key_encrypted = self.receive_and_unpack()
        cipher_key = self.ssl_system.decrypt_message(
            cipher_key_encrypted, public_key, private_key)
        self.aes_system = AESSystem(cipher_key)

    def create_user_account(self, username, password):
        result = database.check_credentials(self.username, password)
        if result:
            return False
        database.create_user(username, password)
        return True

    def receive_user_credentials(self, username, password): # check credentials here
        credentials = self.receive_and_unpack(encrypted=True)

        result = database.check_credentials(username, password)
        if result:
            return True
        return False

    def handle_user_connection(self):
        request = self.receive_and_unpack(encrypted=True)
        self.username = request['username']
        password = request['password']
        print(self.username)
        print(password)
        print(request['request_type'])

        if request['request_type'] == 'create_user':
            print('x')
            return self.create_user_account(self.username, password)

        elif request['request_type'] == 'login':
            print('y')
            return True#self.receive_user_credentials(self.username, password)


class userClientSide(User):
    def __init__(self, connection=None, ip_port=None, username=None, password=None):
        super().__init__(connection, ip_port, username, password)
    
    def key_exchange(self):
        public_key = self.receive_and_unpack()
        aes_key, encrypted_aes = self.ssl_system.generate_message(public_key)
        self.aes_system = AESSystem(int(aes_key))
        self.pack_and_send(encrypted_aes)

    def connect(self, t='login'):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))
        self.key_exchange()
        request = {'request_type':t, 'username':self.username, 'password':self.password}
        self.pack_and_send(request, encrypted=True)
        response = self.receive_and_unpack(encrypted=True)

        if response['response'] == 'Connection failed':
            print('Connection failed')
