import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
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

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a Neo4j session with proper cleanup."""
        if not self.driver:
            self.connect()
        session = self.driver.session()
        try:
            yield session
        finally:
            session.close()