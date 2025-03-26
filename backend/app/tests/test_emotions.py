from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_emotion():
    response = client.post("/emotions", json={"name": "Anxiety"})
    assert response.status_code == 200  # Espera-se que seja 200 ou 201 para sucesso
    assert response.json()["message"] == "Emotion added successfully"
    assert response.json()["emotion"]["name"] == "Anxiety"

def test_get_all_emotions():
    response = client.get("/emotions")
    assert response.status_code == 200
    assert isinstance(response.json()['emotions'], list)  # Verifica se a chave 'emotions' é uma lista

