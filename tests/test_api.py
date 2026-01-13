from fastapi.testclient import TestClient

from backend.app.config import MODEL_PATH
from backend.app.ngram import build_models, build_unigram, save_model
from backend.app.main import app


def _write_test_model():
    corpus = [["ciao", "mondo"], ["ciao", "amico"]]
    models = build_models(corpus, n_values=[2, 3, 4])
    unigram = build_unigram(corpus)
    save_model(MODEL_PATH, models=models, unigram=unigram)


def test_health():
    _write_test_model()
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate():
    _write_test_model()
    client = TestClient(app)
    payload = {
        "mood": "calma",
        "seed": "oggi",
        "max_tokens": 10,
        "n": 3,
        "top_k": 5,
        "temperature": 1.0,
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "used" in data
    assert data["used"]["mood"] == "calma"
