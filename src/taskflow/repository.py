"""Persistência das tarefas em arquivo JSON local (RNF02, RNF03)."""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional

from taskflow.models import Tarefa, ValidacaoError

VERSAO_FORMATO = 1
VARIAVEL_AMBIENTE = "TASKFLOW_ARQUIVO"


class RepositorioError(Exception):
    """Falha ao ler ou gravar o arquivo de dados."""


class ArquivoCorrompidoError(RepositorioError):
    """O arquivo existe, mas não contém dados válidos do TaskFlow."""

    def __init__(self, caminho: Path, backup: Path):
        super().__init__(f"arquivo de dados corrompido: {caminho}")
        self.caminho = caminho
        self.backup = backup


def caminho_padrao() -> Path:
    """Usa TASKFLOW_ARQUIVO, se definida; senão ~/.taskflow/tarefas.json."""
    personalizado = os.environ.get(VARIAVEL_AMBIENTE)
    if personalizado:
        return Path(personalizado).expanduser()
    return Path.home() / ".taskflow" / "tarefas.json"


class RepositorioJSON:
    def __init__(self, caminho: Optional[Path] = None):
        self.caminho = Path(caminho) if caminho else caminho_padrao()

    def carregar(self) -> List[Tarefa]:
        if not self.caminho.exists():
            return []
        try:
            with self.caminho.open(encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except OSError as erro:
            raise RepositorioError(f"não foi possível acessar o arquivo de dados: {erro}") from erro
        except (json.JSONDecodeError, UnicodeDecodeError) as erro:
            raise self._corrompido() from erro
        try:
            return [Tarefa.from_dict(item) for item in dados["tarefas"]]
        except (TypeError, KeyError, ValueError, ValidacaoError) as erro:
            raise self._corrompido() from erro

    def _corrompido(self) -> ArquivoCorrompidoError:
        """Preserva uma cópia do arquivo inválido antes de reportar (RNF03)."""
        backup = self.caminho.with_name(self.caminho.name + ".bak")
        try:
            shutil.copy2(self.caminho, backup)
        except OSError:
            pass
        return ArquivoCorrompidoError(self.caminho, backup)

    def salvar(self, tarefas: List[Tarefa]) -> None:
        """Grava de forma atômica: escreve em um temporário e troca com os.replace."""
        documento = {"versao": VERSAO_FORMATO, "tarefas": [t.to_dict() for t in tarefas]}
        try:
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            fd, temporario = tempfile.mkstemp(
                dir=self.caminho.parent, prefix=".tarefas-", suffix=".tmp"
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as arquivo:
                    json.dump(documento, arquivo, ensure_ascii=False, indent=2)
                    arquivo.write("\n")
                os.replace(temporario, self.caminho)
            except BaseException:
                Path(temporario).unlink(missing_ok=True)
                raise
        except OSError as erro:
            raise RepositorioError(f"não foi possível gravar o arquivo de dados: {erro}") from erro
