"""Interface de linha de comando do TaskFlow."""

import argparse
import sys
from datetime import date
from typing import Callable, List, Optional

from taskflow import __version__
from taskflow.models import Prioridade, Status, ValidacaoError
from taskflow.models import Tarefa
from taskflow.repository import RepositorioError, RepositorioJSON
from taskflow.services import TarefaNaoEncontradaError, TaskService

SUCESSO, ERRO_USO, ERRO_DADOS = 0, 1, 2

PRIORIDADES = [p.value for p in Prioridade]
STATUS = [s.value for s in Status]


def formatar_tabela(tarefas: List[Tarefa], hoje: Optional[date] = None) -> str:
    """Tabela de tarefas; prazos vencidos de tarefas pendentes recebem '!'."""
    if not tarefas:
        return "Nenhuma tarefa encontrada."
    hoje = hoje or date.today()
    cabecalho = ("ID", "STATUS", "PRIORIDADE", "PRAZO", "TÍTULO")
    linhas = []
    for t in tarefas:
        prazo = t.prazo.isoformat() if t.prazo else "-"
        if t.esta_atrasada(hoje):
            prazo += "!"
        linhas.append((str(t.id), t.status.value, t.prioridade.value, prazo, t.titulo))
    larguras = [max(len(linha[i]) for linha in [cabecalho, *linhas]) for i in range(4)]

    def montar(colunas):
        return "  ".join(c.ljust(w) for c, w in zip(colunas[:4], larguras)) + "  " + colunas[4]

    saida = [montar(cabecalho), montar(tuple("-" * w for w in larguras) + ("-" * 6,))]
    saida += [montar(linha) for linha in linhas]
    rodape = f"\n{len(tarefas)} tarefa(s)."
    if any(t.esta_atrasada(hoje) for t in tarefas):
        rodape += "   (! = atrasada)"
    return "\n".join(saida) + rodape


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

    p = sub.add_parser("listar", help="listar tarefas, com filtros opcionais")
    p.add_argument("-s", "--status", choices=STATUS)
    p.add_argument("-p", "--prioridade", choices=PRIORIDADES)
    p.set_defaults(func=cmd_listar)

    p = sub.add_parser("editar", help="alterar campos de uma tarefa")
    p.add_argument("id", type=int)
    p.add_argument("-t", "--titulo")
    p.add_argument("-d", "--descricao")
    p.add_argument("-p", "--prioridade", choices=PRIORIDADES)
    prazo = p.add_mutually_exclusive_group()
    prazo.add_argument("--prazo", help="novo prazo no formato AAAA-MM-DD")
    prazo.add_argument("--sem-prazo", action="store_true", help="remover o prazo")
    p.set_defaults(func=cmd_editar)
    return parser


def cmd_adicionar(servico: TaskService, args, entrada) -> int:
    tarefa = servico.adicionar(
        args.titulo, descricao=args.descricao, prioridade=args.prioridade, prazo=args.prazo
    )
    print(f"Tarefa {tarefa.id} criada: {tarefa.titulo}")
    return SUCESSO


def cmd_listar(servico: TaskService, args, entrada) -> int:
    tarefas = servico.listar(status=args.status, prioridade=args.prioridade)
    print(formatar_tabela(tarefas, servico.hoje()))
    return SUCESSO


def cmd_editar(servico: TaskService, args, entrada) -> int:
    campos = (args.titulo, args.descricao, args.prioridade, args.prazo)
    if all(c is None for c in campos) and not args.sem_prazo:
        print(
            "Nada para alterar. Informe --titulo, --descricao, --prioridade, --prazo ou --sem-prazo.",
            file=sys.stderr,
        )
        return ERRO_USO
    servico.editar(
        args.id,
        titulo=args.titulo,
        descricao=args.descricao,
        prioridade=args.prioridade,
        prazo=args.prazo,
        remover_prazo=args.sem_prazo,
    )
    print(f"Tarefa {args.id} atualizada.")
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
