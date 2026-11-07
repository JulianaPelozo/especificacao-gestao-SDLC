"""Modelo de domínio do TaskFlow: a entidade Tarefa e suas validações."""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional

TITULO_MAX = 120


class ValidacaoError(ValueError):
    """Dados de entrada inválidos para uma tarefa (RNF05)."""


class Prioridade(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"

    @property
    def peso(self) -> int:
        """Peso usado para ordenar (maior = mais urgente)."""
        return {"baixa": 1, "media": 2, "alta": 3}[self.value]


class Status(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"


def validar_titulo(titulo: str) -> str:
    """Remove espaços das pontas (RN04) e valida o título (RF01)."""
    titulo = (titulo or "").strip()
    if not titulo:
        raise ValidacaoError("o título não pode ser vazio.")
    if len(titulo) > TITULO_MAX:
        raise ValidacaoError(f"o título deve ter no máximo {TITULO_MAX} caracteres.")
    return titulo


def parse_prioridade(valor) -> Prioridade:
    if isinstance(valor, Prioridade):
        return valor
    try:
        return Prioridade(str(valor).strip().lower())
    except ValueError:
        opcoes = ", ".join(p.value for p in Prioridade)
        raise ValidacaoError(f"prioridade inválida '{valor}'. Use: {opcoes}.") from None


def parse_prazo(valor) -> Optional[date]:
    """Converte 'AAAA-MM-DD' em date. None ou texto vazio significam sem prazo."""
    if valor is None or isinstance(valor, date):
        return valor
    texto = str(valor).strip()
    if not texto:
        return None
    try:
        return date.fromisoformat(texto)
    except ValueError:
        raise ValidacaoError(
            f"prazo inválido '{valor}'. Use o formato AAAA-MM-DD (ex.: 2026-11-14)."
        ) from None


