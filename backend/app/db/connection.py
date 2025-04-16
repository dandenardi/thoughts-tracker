import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, exceptions
from contextlib import contextmanager
from typing import Generator
from neo4j._sync.driver import Session

load_dotenv()

# Load environment variables
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class Neo4jConnection:
    def __init__(self, uri: str = NEO4J_URI, user: str = NEO4J_USER, password: str = NEO4J_PASSWORD):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.connect()

    def connect(self) -> bool:
        """Establishes Neo4j connection and returns a status."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            print("Connection established.")
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j: {str(e)}")
            return False

    def close(self):
        """Close the Neo4j driver connection."""
        if self.driver:
            self.driver.close()
            print("Connection closed.")

    def reconnect(self):
        """
        Attempt to reconnect to the Neo4j database.
        """

        print("Attempting to reconnect...")
        self.close()
        return self.connect()

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a Neo4j session with automatic reconnection on failure."""
        if not self.driver or self.driver is None:
            self.connect()

        
        try:
            session = self.driver.session()
            yield session
        except exceptions.SessionExpired:
            print("Session expired, attempting to reconnect...")
            if self.reconnect():
                session = self.driver.session()
                yield session
            else:
                raise Exception("Failed to reconnect to Neo4j after session expiration.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if session:
                session.close()