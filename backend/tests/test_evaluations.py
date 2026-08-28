from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_valid_evaluation():
    payload = {
        "prompt": "Explain what RAG is.",
        "response": "RAG combines retrieval with generation.",
        "score": 9,
        "feedback": "Accurate and concise explanation."
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["prompt"] == payload["prompt"]
    assert data["response"] == payload["response"]
    assert data["score"] == payload["score"]
    assert data["feedback"] == payload["feedback"]


def test_create_evaluation_auto_generated_id():
    payload_1 = {
        "prompt": "Prompt 1",
        "response": "Response 1",
        "score": 8,
        "feedback": "Feedback 1"
    }
    payload_2 = {
        "prompt": "Prompt 2",
        "response": "Response 2",
        "score": 7,
        "feedback": "Feedback 2"
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


def test_list_evaluations():
    # Get initial list
    response_list_before = client.get("/evaluations")
    assert response_list_before.status_code == 200
    list_before = response_list_before.json()
    assert isinstance(list_before, list)

    payload = {
        "prompt": "Testing list.",
        "response": "Response for list testing.",
        "score": 5,
        "feedback": "Neutral response."
    }
    create_response = client.post("/evaluations", json=payload)
    assert create_response.status_code == 201
    created_id = create_response.json()["id"]

    response_list_after = client.get("/evaluations")
    assert response_list_after.status_code == 200
    list_after = response_list_after.json()
    assert isinstance(list_after, list)
    assert len(list_after) > len(list_before)
    
    # Check if the created item is in the list
    found = False
    for item in list_after:
        if item.get("id") == created_id:
            found = True
            assert item["prompt"] == payload["prompt"]
            assert item["response"] == payload["response"]
            assert item["score"] == payload["score"]
            assert item["feedback"] == payload["feedback"]
            break
    assert found


def test_get_evaluation_by_id():
    payload = {
        "prompt": "Get by ID testing.",
        "response": "Specific response content.",
        "score": 10,
        "feedback": "Perfect response."
    }
    create_response = client.post("/evaluations", json=payload)
    assert create_response.status_code == 201
    created_id = create_response.json()["id"]

    response = client.get(f"/evaluations/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id
    assert data["prompt"] == payload["prompt"]
    assert data["response"] == payload["response"]
    assert data["score"] == payload["score"]
    assert data["feedback"] == payload["feedback"]


def test_get_evaluation_by_id_not_found():
    response = client.get("/evaluations/non-existent-id-12345")
    assert response.status_code == 404


def test_create_evaluation_score_below_zero():
    payload = {
        "prompt": "Invalid score.",
        "response": "Response.",
        "score": -1,
        "feedback": "Score below zero."
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_score_above_ten():
    payload = {
        "prompt": "Invalid score.",
        "response": "Response.",
        "score": 11,
        "feedback": "Score above ten."
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_missing_prompt():
    payload = {
        "response": "Response.",
        "score": 5,
        "feedback": "No prompt."
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_missing_response():
    payload = {
        "prompt": "Prompt.",
        "score": 5,
        "feedback": "No response."
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_missing_score():
    payload = {
        "prompt": "Prompt.",
        "response": "Response.",
        "feedback": "No score."
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422


def test_create_evaluation_missing_feedback():
    payload = {
        "prompt": "Prompt.",
        "response": "Response.",
        "score": 5
    }
    response = client.post("/evaluations", json=payload)
    assert response.status_code == 422

