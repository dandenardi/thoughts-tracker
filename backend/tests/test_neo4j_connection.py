import pytest
from app.db.connection import Neo4jConnection

@pytest.fixture
def neo4j_connection():
    connection = Neo4jConnection()
    yield connection
    connection.close()  # Fecha a conexão após o teste

def test_neo4j_connection(neo4j_connection):
    # Verifique se a conexão foi estabelecida com sucesso, verificando o retorno de 'connect()'
    assert neo4j_connection.connect() is True  # A conexão deve retornar True se for bem-sucedida
