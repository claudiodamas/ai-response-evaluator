from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.llm_judge import evaluate_pairwise

client = TestClient(app)


def test_create_valid_pairwise_evaluation():
    payload = {
        "query": "Qual é a capital do Brasil?",
        "left_response": "A capital do Brasil é Brasília.",
        "right_response": "A capital do Brasil é Buenos Aires."
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "user_email" in data
    assert data["query"] == payload["query"]
    assert data["left_response"] == payload["left_response"]
    assert data["right_response"] == payload["right_response"]
    assert "left_score" in data
    assert "right_score" in data
    assert "comment" in data
    assert isinstance(data["left_score"], (int, float))
    assert isinstance(data["right_score"], (int, float))
    assert isinstance(data["comment"], str)


def test_create_evaluation_with_mocked_llm():
    mock_llm_result = {
        "left_score": 9.5,
        "right_score": 2.0,
        "comment": "A resposta esquerda é precisa e completa, enquanto a direita contém erros conceituais."
    }
    payload = {
        "query": "Explique o conceito de RAG.",
        "left_response": "RAG combina recuperação de documentos com geração por LLM.",
        "right_response": "RAG é um tipo de banco de dados relacional antigo."
    }
    
    with patch("app.main.evaluate_pairwise", return_value=mock_llm_result):
        response = client.post("/evaluations", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["left_score"] == 9.5
        assert data["right_score"] == 2.0
        assert data["comment"] == mock_llm_result["comment"]


def test_create_evaluation_auto_generated_id():
    payload_1 = {
        "query": "Pergunta 1",
        "left_response": "Resposta 1A",
        "right_response": "Resposta 1B"
    }
    payload_2 = {
        "query": "Pergunta 2",
        "left_response": "Resposta 2A",
        "right_response": "Resposta 2B"
    }
    
    response_1 = client.post("/evaluations", json=payload_1)
    response_2 = client.post("/evaluations", json=payload_2)
    
    assert response_1.status_code == 201
    assert response_2.status_code == 201
    
    id_1 = response_1.json().get("id")
    id_2 = response_2.json().get("id")
    
    assert id_1 is not None
    assert id_2 is not None
    assert id_1 != id_2
    assert isinstance(id_1, str)
    assert isinstance(id_2, str)
    assert len(id_1) > 0
    assert len(id_2) > 0


def test_create_evaluation_missing_query():
    payload = {
        "left_response": "Resposta Esquerda",
        "right_response": "Resposta Direita"
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_missing_left_response():
    payload = {
        "query": "Qual é a capital?",
        "right_response": "Resposta Direita"
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_missing_right_response():
    payload = {
        "query": "Qual é a capital?",
        "left_response": "Resposta Esquerda"
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_empty_or_whitespace_fields():
    # Empty query
    response_empty_query = client.post("/evaluations", json={
        "query": "   ",
        "left_response": "Resposta",
        "right_response": "Resposta"
    })
    assert response_empty_query.status_code == 422

    # Empty left_response
    response_empty_left = client.post("/evaluations", json={
        "query": "Pergunta",
        "left_response": "",
        "right_response": "Resposta"
    })
    assert response_empty_left.status_code == 422

    # Empty right_response
    response_empty_right = client.post("/evaluations", json={
        "query": "Pergunta",
        "left_response": "Resposta",
        "right_response": "   "
    })
    assert response_empty_right.status_code == 422


def test_get_history_by_email():
    payload = {
        "query": "Histórico Teste",
        "left_response": "Resp Esquerda Histórico",
        "right_response": "Resp Direita Histórico"
    }
    create_response = client.post("/evaluations", json=payload)
    assert create_response.status_code == 201
    created_id = create_response.json()["id"]

    # Query history for static default user
    response = client.get("/evaluations/history?email=user@example.com")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) > 0
    
    # Verify the created evaluation exists in the user history
    found = any(item.get("id") == created_id for item in history)
    assert found


def test_get_history_empty_for_unknown_email():
    response = client.get("/evaluations/history?email=unknown_user_123@example.com")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) == 0


def test_llm_judge_fallback():
    # When no API key is provided, evaluate_pairwise should return a safe fallback dictionary
    result = evaluate_pairwise("Query teste", "Resp A", "Resp B")
    assert "left_score" in result
    assert "right_score" in result
    assert "comment" in result
    assert isinstance(result["left_score"], (int, float))
    assert isinstance(result["right_score"], (int, float))
