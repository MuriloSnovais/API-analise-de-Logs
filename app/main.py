import ipaddress

from fastapi import FastAPI, Query
from pydantic import BaseModel, field_validator

from app.services import analyze_logs_with_ai, suspect_logs

app = FastAPI(
    title="API de Análise de Logs",
    description="Marca como suspeito o IP com 5 ou mais falhas de login.",
)


class LogBase(BaseModel):
    ip: str
    login: str

    @field_validator("ip")
    @classmethod
    def must_be_ip(cls, value: str) -> str:
        cleaned = value.strip()
        ipaddress.ip_address(cleaned)
        return cleaned

    @field_validator("login")
    @classmethod
    def must_be_status(cls, value: str) -> str:
        cleaned = value.strip().lower()
        allowed = {"failed", "fail", "failure", "success", "sucess", "ok"}
        if cleaned not in allowed:
            raise ValueError("login deve ser failed ou success")
        return cleaned


@app.get("/")
def health():
    return {"status": "API online"}


@app.post("/analise")
@app.post("/analyse")
def take_log(data: list[LogBase], with_ai: bool = Query(False)):
    suspects = suspect_logs(data)
    if not with_ai:
        return suspects
    return {"suspects": suspects, "ai": analyze_logs_with_ai(suspects)}
