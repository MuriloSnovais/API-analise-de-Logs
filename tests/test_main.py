from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_ips = [{"ip": "191.194.129.227", "login": "sucess"}, {"ip": "187.32.150.118", "login": "sucess"}]
test_suspects_ips = [{
    "ip": "177.127.122.97", "login": "failed"
  },
  {
    "ip": "177.127.122.97", "login": "failed"
  },
  {
    "ip": "177.127.122.97", "login": "failed"
  },
  {
    "ip": "177.127.122.97", "login": "failed"
  },
  {
    "ip": "177.127.122.97", "login": "failed"
  },
  {
    "ip": "177.127.122.97", "login": "failed"
  },
]


def test_post_main_suspects():
    response = client.post("/analise", json=test_suspects_ips)
    assert response.status_code == 200
    body = response.json()
    assert body[0]["Suspect IP"] == "177.127.122.97"
    assert body[0]["Try"] == 6
    assert body[0]["successful_attempts"] == 0
    assert body[0]["risk"] == "high"


def test_post_main_positive():
    response = client.post("/analise", json=test_ips)
    assert response.status_code == 200
    assert response.json() == []


def test_four_failures_are_not_suspect():
    logs = [{"ip": "10.0.0.8", "login": "failed"} for _ in range(4)]
    response = client.post("/analise", json=logs)
    assert response.status_code == 200
    assert response.json() == []


def test_invalid_ip_is_rejected():
    response = client.post("/analise", json=[{"ip": "nao-e-ip", "login": "failed"}])
    assert response.status_code == 422


def test_ai_without_key_keeps_the_rule(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    response = client.post("/analise", params={"with_ai": True}, json=test_suspects_ips)
    assert response.status_code == 200
    body = response.json()
    assert body["suspects"][0]["Try"] == 6
    assert body["ai"]["enabled"] is False
    


def test_ai_summary_uses_already_classified_ips(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    def fake_summary(prompt):
        assert "177.127.122.97" in prompt
        return '{"summary":"Possível força bruta.","recommendations":["Bloquear o IP temporariamente"]}'

    monkeypatch.setattr("app.services._generate_summary", fake_summary)
    response = client.post("/analyse", params={"with_ai": True}, json=test_suspects_ips)
    assert response.status_code == 200
    body = response.json()
    assert body["ai"]["enabled"] is True
    assert body["ai"]["summary"] == "Possível força bruta."
    assert body["ai"]["recommendations"] == ["Bloquear o IP temporariamente"]



