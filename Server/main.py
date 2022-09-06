import os
import yaml
from server import Server
import sys

sys.path.insert(1, r'C:\Users\ahuma\Desktop\Programming\python_programs\Misc Projects\New-chat-server\classes')
from User import userServerSide
from Initializer import initializer


if __name__ == '__main__':
    initializer = initializer()
    attributes = initializer.get_attributes(r'C:\Users\ahuma\Desktop\Programming\python_programs\Misc Projects\New-chat-server\Server\server-conf.yaml')
    server = Server(**attributes)
    server.main()

