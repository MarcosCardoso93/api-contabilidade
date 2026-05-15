import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_listar_lancamentos(client):
    response = client.get("/lancamentos/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_detalhar_lancamento_existente(client):
    response = client.get("/lancamentos/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1


def test_detalhar_lancamento_inexistente(client):
    response = client.get("/lancamentos/9999")
    assert response.status_code == 404


def test_criar_lancamento(client):
    response = client.post(
        "/lancamentos/",
        json={
            "descricao": "Pagamento de fornecedor",
            "tipo": "debito",
            "valor": 500.00,
            "data": "2026-05-15",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["descricao"] == "Pagamento de fornecedor"
    assert data["tipo"] == "debito"


def test_criar_lancamento_tipo_invalido(client):
    response = client.post(
        "/lancamentos/",
        json={
            "descricao": "Teste",
            "tipo": "invalido",
            "valor": 100.00,
            "data": "2026-05-15",
        },
    )
    assert response.status_code == 400


def test_criar_lancamento_sem_campos(client):
    response = client.post("/lancamentos/", json={})
    assert response.status_code == 400
