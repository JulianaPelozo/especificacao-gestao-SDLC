"""Interface de linha de comando do TaskFlow."""

import argparse
import sys
from typing import Callable, List, Optional

from taskflow import __version__
from taskflow.models import Prioridade, Status, ValidacaoError
from taskflow.repository import RepositorioError, RepositorioJSON
from taskflow.services import TarefaNaoEncontradaError, TaskService

SUCESSO, ERRO_USO, ERRO_DADOS = 0, 1, 2

PRIORIDADES = [p.value for p in Prioridade]
STATUS = [s.value for s in Status]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskflow",
        description="Mini-gerenciador de tarefas de linha de comando.",
        epilog="Os dados ficam em ~/.taskflow/tarefas.json (altere com TASKFLOW_ARQUIVO).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="comando", metavar="<comando>")

    p = sub.add_parser("adicionar", help="cadastrar uma nova tarefa")
    p.add_argument("titulo", help="título da tarefa")
    p.add_argument("-d", "--descricao", default="", help="descrição opcional")
    p.add_argument("-p", "--prioridade", choices=PRIORIDADES, default="media")
    p.add_argument("--prazo", help="data limite no formato AAAA-MM-DD")
    p.set_defaults(func=cmd_adicionar)
    return parser


def cmd_adicionar(servico: TaskService, args, entrada) -> int:
    tarefa = servico.adicionar(
        args.titulo, descricao=args.descricao, prioridade=args.prioridade, prazo=args.prazo
    )
    print(f"Tarefa {tarefa.id} criada: {tarefa.titulo}")
    return SUCESSO


def main(
    argv: Optional[List[str]] = None,
    servico: Optional[TaskService] = None,
    entrada: Callable[[str], str] = input,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return SUCESSO
    servico = servico or TaskService(RepositorioJSON())
    try:
        return args.func(servico, args, entrada)
    except (ValidacaoError, TarefaNaoEncontradaError) as erro:
        print(f"Erro: {erro.args[0]}", file=sys.stderr)
        return ERRO_USO
    except RepositorioError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return ERRO_DADOS
