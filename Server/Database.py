import py2neo
from py2neo import Graph
import hashlib


class Database:
    def __init__(self, graph):
        self.graph = graph

    def check_credentials(self, username, password):
        password = hashlib.sha256(password.encode('utf-8')).digest()
        print(password)
        check_credentials = "MATCH (u:USER" + " {" f'username:"{username}", password:"{password}"' + "})" + "RETURN u"

        return_value = self.graph.run(check_credentials)

        if str(return_value) == '(No data)':
            return False
        return True

    def create_user(self, username, password):
        result = self.check_credentials(username, password)

        if result:
            return "User already exists"
        
        else:
            password = hashlib.sha256(password.encode('utf-8')).digest()
            create_user = "CREATE (u:USER" + " {" f'username:"{username}", password:"{password}"' + "})"

            self.graph.run(create_user)


# if __name__ == "__main__":
#     database = Database('neo4j+s://33cee990.databases.neo4j.io:7687', 'neo4j', '3rhoAmtSTX-7bfvV3eVCR2VqhRg_45_rbBdK6Tr5NGM')
#     database.create_user("sugma", "TEST")