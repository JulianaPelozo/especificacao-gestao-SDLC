"""Camada de aplicação: implementa os casos de uso sobre as tarefas."""

from datetime import date, datetime
from typing import Callable, List, Optional

from taskflow.models import Prioridade, Status, Tarefa, parse_prioridade
from taskflow.repository import RepositorioJSON


class TarefaNaoEncontradaError(LookupError):
    def __init__(self, tarefa_id: int):
        super().__init__(f"Tarefa {tarefa_id} não encontrada.")
        self.tarefa_id = tarefa_id


class TaskService:
    def __init__(
        self,
        repositorio: RepositorioJSON,
        relogio: Optional[Callable[[], datetime]] = None,
    ):
        self.repositorio = repositorio
        self.relogio = relogio or datetime.now

    def hoje(self) -> date:
        return self.relogio().date()

    @staticmethod
    def _localizar(tarefas: List[Tarefa], tarefa_id: int) -> Tarefa:
        for tarefa in tarefas:
            if tarefa.id == tarefa_id:
                return tarefa
        raise TarefaNaoEncontradaError(tarefa_id)

    def adicionar(
        self,
        titulo: str,
        descricao: str = "",
        prioridade=Prioridade.MEDIA,
        prazo=None,
    ) -> Tarefa:
        """UC01 — o ID é o maior existente + 1 e nunca é reutilizado (RN01)."""
        tarefas = self.repositorio.carregar()
        proximo_id = max((t.id for t in tarefas), default=0) + 1
        tarefa = Tarefa(
            id=proximo_id,
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            prazo=prazo,
            criada_em=self.relogio().replace(microsecond=0),
        )
        tarefas.append(tarefa)
        self.repositorio.salvar(tarefas)
        return tarefa

    def listar(
        self,
        status: Optional[str] = None,
        prioridade: Optional[str] = None,
    ) -> List[Tarefa]:
        """UC02 — lista com filtros opcionais por status e prioridade (RF02, RF03)."""
        tarefas = self.repositorio.carregar()
        if status:
            tarefas = [t for t in tarefas if t.status is Status(status)]
        if prioridade:
            alvo = parse_prioridade(prioridade)
            tarefas = [t for t in tarefas if t.prioridade is alvo]
        return sorted(tarefas, key=lambda t: t.id)
