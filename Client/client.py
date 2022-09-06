import json
import socket
import sys
import keyring
import getpass

sys.path.insert(0, r'C:\Users\ahuma\Desktop\Programming\python_programs\Misc Projects\New-chat-server\encryption-algorithms')
from SSL import SSLSystem
from AES import AESSystem
sys.path.insert(1, r'C:\Users\ahuma\Desktop\Programming\python_programs\Misc Projects\New-chat-server\classes')
from User import userClientSide
from Initializer import initializer


class Client:
    def __init__(self, IP, PORT, username, password, request_type='login'):
        self.user = userClientSide(ip_port=(IP, PORT), username=username, password=password)
        self.username, self.ip = username, IP
        self.request_type = request_type
    
    def connect(self):
        try:
            self.user.connect(t=self.request_type)
        except ConnectionRefusedError:
            print(f'Connection failure')
                

if __name__ == "__main__":
    username = str(input('Username: '))
    if keyring.get_password('chat_server', username):
        password = keyring.get_password('chat_server', username)
    else:
        password = getpass.getpass("password: ")
        password_save_decision = str(input("Would you like to save your password? [y/n]")).lower()
        if password_save_decision == 'y':
            keyring.set_password('chat_server', username, password)
        elif password_save_decision == 'n':
            print('Ok, not saving')

    initializer = initializer()
    config = initializer.get_attributes(r'C:\Users\ahuma\Desktop\Programming\python_programs\Misc Projects\New-chat-server\Client\client-conf.yml')

    client = Client(config['ip'], config['port'], username, password)
    client.connect()




