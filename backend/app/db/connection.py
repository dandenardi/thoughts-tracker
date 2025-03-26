import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

# Carregar as variáveis de ambiente
NEO4J_URI = os.getenv("NEO4J_URI")  
NEO4J_USER = os.getenv("NEO4J_USERNAME")  # Alterado para o nome correto
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jConnection:
    def __init__(self, uri: str = NEO4J_URI, user: str = NEO4J_USER, password: str = NEO4J_PASSWORD):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        
        self.connect()

    def connect(self):
        """Establishes Neo4j connection."""
        try:
            # Tentando se conectar ao banco de dados Neo4j
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            print("Connection established.")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {str(e)}")

    def close(self):
        """Closes the Neo4j connection."""
        if self.driver:
            self.driver.close()
            print("Connection closed.")

    def get_session(self):
        """Returns an active session for performing queries."""
        if not self.driver:
            self.connect()
        return self.driver.session()

# Exemplo de uso:
# db = Neo4jConnection()
# session = db.get_session()
