import socket
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

sys.path.insert(0, r'C:\Users\ahuma\Desktop\Programming\python_programs\Misc Projects\New-chat-server\encryption-algorithms')
from SSL import SSLSystem
from AES import AESSystem
sys.path.insert(1, r'C:\Users\ahuma\Desktop\Programming\python_programs\Misc Projects\New-chat-server\classes')
from User import userServerSide
from killable_thread import ServerThread


class Server:
    def __init__(self, **kwargs):#IP, PORT, db_link, db_username, db_password):
        sys_log_file = filename = os.path.join(r'system_logs.txt')
        msg_log_file = filename = os.path.join(r'message_logs.txt')

        self.IP = kwargs['ip']
        self.PORT = kwargs['port']
        self.connections = []
        self.message_queue = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.IP, self.PORT))
        self.sock.listen(50)

        self.connections_lock = multiprocessing.Lock()
        self.message_lock = multiprocessing.Lock()

        graph = Graph(kwargs['dbLink'], auth=(kwargs['dbUsername'], kwargs['dbPassword']), secure=True, verify=True)
        self.database = Database(graph)

        print('[+] Initialized')

    def accept_users(self):
        print("[+] Accepting Users")
        while True:
            print("At top of loop")
            response = {'response':None}
            connection, ip_port = self.sock.accept()
            user = userServerSide(connection=connection, ip_port=ip_port, database=self.database)
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
            user_dict = {'user':user,
                         'receive':ServerThread(target=self.receive, args=[user]), 
                         'send':ServerThread(target=self.send, args=[user]), 
                         'ping':ServerThread(target=user.ping_connection, args=(send_thread, receive_thread))
                        }
            user_dict['receive'].start()
            user_dict['send'].start()
            user_dict['ping'].start()

            with self.connections_lock:
                self.connections.append(user_dict)
            print('user connected')
            print(self.connections)
            
    def receive(self, user):
        while True:
            with self.message_lock:
                message = user.receive_and_unpack(encrypted=True)
                with self.message_lock:
                    self.message_queue.append(message)
                print(message)

    def send(self, user):
        while True:
            with self.message_lock:
                for message in self.message_queue:
                    user.pack_and_send(message, encrypted=True)
                    self.message_queue.remove(message)
                    time.sleep(0.05)
        
    def cancel_connection(connection):
        if not connection['receive'].is_alive():
            connection['ping'].kill()
            del connection['user']

            connection['receive'].join()
            connection['send'].join()
            connection['ping'].join()

            with self.connections_lock:
                self.connections.remove(connection)
            
    def canceller(self):
        while True:
            for connection in self.connections:
                self.cancel_connection(connection)

    def main(self):
        connect = ServerThread(target=self.accept_users)
        cancel = ServerThread(target=self.canceller)
        connect.start()
        cancel.start()

        

# if __name__ == "__main__":
    
#     server = Server(r'server-conf.yaml')
#     asyncio.run(server.main())

