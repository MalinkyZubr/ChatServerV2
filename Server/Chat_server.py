import socket
import asyncio
import multiprocessing
import ssl
import json
import os
import threading
import py2neo
from py2neo import Graph
from Database import Database
import yaml
import sys
import time

sys.path.insert(0, r'New-chat-server\encryption-algorithms')
from SSL import SSLSystem
from AES import AESSystem
sys.path.insert(1, r'New-chat-server\classes')
from User import userServerSide

pwd = os.path.dirname(os.path.abspath(__file__))
conf_file = os.path.join(pwd, r'server-conf.yaml')
with open(conf_file, 'r') as cf:
    data = yaml.load(cf, Loader=yaml.FullLoader)
    link = data[0]['Database']['link']
    username = data[0]['Database']['username']
    password = data[0]['Database']['password']

graph = Graph(link, auth=(username, password), secure=True, verify=True)
database = Database(graph)

#
    # class User:
    #     def __init__(self, connection=None, ip_port=None):
    #         self.connection = connection
    #         self.ip, self.port = ip_port
    #         self.username = None
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
    #         private_key, public_key = self.ssl_system.create_keys()
    #         print(public_key)
    #         self.pack_and_send(public_key)
    #         cipher_key_encrypted = self.receive_and_unpack()
    #         cipher_key = self.ssl_system.decrypt_message(
    #             cipher_key_encrypted, public_key, private_key)
    #         self.aes_system = AESSystem(cipher_key)

    #     def create_user_account(self, username, password):
    #         result = database.check_credentials(self.username, password)
    #         if result:
    #             return False
    #         database.create_user(username, password)
    #         return True

    #     def receive_user_credentials(self, username, password): # check credentials here
    #         credentials = self.receive_and_unpack(encrypted=True)

    #         result = database.check_credentials(username, password)
    #         if result:
    #             return True
    #         return False

    #     def handle_user_connection(self):
    #         request = self.receive_and_unpack(encrypted=True)
    #         self.username = request['username']
    #         password = request['password']
    #         print(self.username)
    #         print(password)
    #         print(request['request_type'])

    #         if request['request_type'] == 'create_user':
    #             print('x')
    #             return self.create_user_account(self.username, password)

    #         elif request['request_type'] == 'login':
    #             print('y')
    #             return True#self.receive_user_credentials(self.username, password)


class Server:
    def __init__(self, IP, PORT, link, username, password):
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

        self.connections_lock = multiprocessing.Lock()
        self.message_lock = multiprocessing.Lock()

        print('[+] Initialized')

    def accept_users(self):
        print("[+] Accepting Users")
        while True:
            response = {'response':None}
            connection, ip_port = self.sock.accept()
            user = userServerSide(connection=connection, ip_port=ip_port)
            user.key_exchange()
            
            print('GOT HERE')
            auth_state = user.handle_user_connection()
            print(auth_state)
            if not auth_state:
                print("FAILED")
                response['response'] = 'Connection failed'
                user.pack_and_send(response)
                user.connection.close()
                del user
                continue
            else:
                print('SUCCESS1')
            print("SUCCESS")
            response['response'] = 'Connection success'
            user.pack_and_send(response)
            print('GOT HERE2')
            # user_thread = threading.Thread(target=await self.userio, args=[user])
            # user_thread.start()
            coroutine = asyncio.create_task(self.userio(user))
            with self.connections_lock:
                self.connections.append(coroutine)
            print('user connected')
            print(self.connections)
            
    async def receive(self, user):
        while True:
            with self.message_lock:
                message = await user.receive_and_unpack(encrypted=True)
                self.message_queue.append(message)
                print(self.message)

    async def send(self, user):
        while True:
            with self.message_lock:
                for message in self.message_queue:
                    await user.pack_and_send(message, encrypted=True)

    async def userio(self, user):
        send_task = asyncio.create_task(self.send(user))
        receive_task = asyncio.create_task(self.receive(user))

        await send_task
        await receive_task

    async def main(self):
        threads = [self.accept_users()]
        list(map(lambda x: threading.Thread(target=x).start(), threads))

        time.sleep(15)
        await asyncio.gather(*self.connections)
        

if __name__ == "__main__":
    server = Server('192.168.0.173', 4444, 'neo4j+s://33cee990.databases.neo4j.io:7687', 'neo4j', '3rhoAmtSTX-7bfvV3eVCR2VqhRg_45_rbBdK6Tr5NGM')
    asyncio.run(server.main())

