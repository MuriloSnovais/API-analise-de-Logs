"""Motor de análise de logs de login.

A classificação de suspeito é uma regra fixa: 5 ou mais falhas.
A IA não conta tentativas. Ela só explica os IPs que a regra já marcou.
"""

from collections import defaultdict
import json
import os

SUSPECT_THRESHOLD = 5
FAILED_STATUSES = {"failed", "fail", "failure"}
SUCCESS_STATUSES = {"success", "sucess", "ok"}


def suspect_logs(receive_data, threshold: int = SUSPECT_THRESHOLD):
    failures = defaultdict(int)
    successes = defaultdict(int)

    for event in receive_data:
        ip = str(event.ip).strip()
        status = _status(event.login)
        if status == "failed":
            failures[ip] += 1
        elif status == "success":
            successes[ip] += 1

    suspects = []
    for ip, failed_count in failures.items():
        if failed_count < threshold:
            continue
        success_count = successes[ip]
        total = failed_count + success_count
        suspects.append(
            {
                "Suspect IP": ip,
                "Try": failed_count,
                "successful_attempts": success_count,
                "failure_rate": round(failed_count / total, 2),
                "risk": _risk(failed_count, success_count, threshold),
            }
        )

    suspects.sort(key=lambda item: item["Try"], reverse=True)
    return suspects


def analyze_logs_with_ai(suspects):
    """Resume os suspeitos já classificados. Nunca altera a lista."""
    if not suspects:
        return {
            "enabled": True,
            "summary": "Nenhum IP atingiu o limite de falhas.",
            "recommendations": [],
        }

    if not _api_key():
        return {
            "enabled": False,
            "summary": None,
            "recommendations": [],
            "detail": "Defina a variável GEMINI_API_KEY para gerar o resumo com IA.",
        }

    try:
        raw = _generate_summary(_prompt(suspects))
    except Exception as exc:
        return {
            "enabled": False,
            "summary": None,
            "recommendations": [],
            "detail": f"A IA não respondeu: {exc.__class__.__name__}",
        }

    return _parse_ai_response(raw)


def _status(login: str) -> str:
    value = login.strip().lower()
    if value in FAILED_STATUSES:
        return "failed"
    if value in SUCCESS_STATUSES:
        return "success"
    return value


def _risk(failed_count: int, success_count: int, threshold: int) -> str:
    if failed_count >= threshold * 2 or success_count == 0:
        return "high"
    return "medium"


def _api_key():
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def _prompt(suspects) -> str:
    payload = json.dumps(suspects, ensure_ascii=False)
    return (
        "Você é um analista de segurança. Os IPs abaixo já foram classificados "
        "por uma regra fixa: 5 ou mais falhas de login. Não altere essa classificação "
        "e não invente eventos. Responda apenas JSON com as chaves "
        "summary (string curta em português) e recommendations (lista de até 3 strings).\n"
        f"Dados: {payload}"
    )


def _generate_summary(prompt: str) -> str:
    from google import genai

    client = genai.Client(api_key=_api_key())
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(model=model, contents=prompt)
    return (response.text or "").strip()


def _parse_ai_response(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {"enabled": True, "summary": raw.strip(), "recommendations": []}

    summary = data.get("summary")
    recommendations = data.get("recommendations") or []
    if not isinstance(summary, str):
        summary = raw.strip()
    if not isinstance(recommendations, list):
        recommendations = []

    return {
        "enabled": True,
        "summary": summary,
        "recommendations": [str(item) for item in recommendations[:3]],
    }
