import os
import yaml
import asyncio
from server import Server

sys.path.insert(1, r'New-chat-server\classes')
from User import userServerSide


if __name__ == '__main__':
    attributes = get_attributes(r'New-chat-server\Server\server-conf.yaml')
    server = Server(**attributes)
    asyncio.run(server.main())

