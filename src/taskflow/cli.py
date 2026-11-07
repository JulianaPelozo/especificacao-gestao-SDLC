"""Interface de linha de comando do TaskFlow."""

import argparse
import sys
from typing import Callable, List, Optional

from taskflow import __version__
from taskflow.formatters import formatar_resumo, formatar_tabela
from taskflow.models import Prioridade, Status, ValidacaoError
from taskflow.repository import ArquivoCorrompidoError, RepositorioError, RepositorioJSON
from taskflow.services import TarefaNaoEncontradaError, TaskService
from taskflow.services import CRITERIOS_ORDENACAO

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

    p = sub.add_parser("listar", help="listar tarefas, com filtros opcionais")
    p.add_argument("-s", "--status", choices=STATUS)
    p.add_argument("-p", "--prioridade", choices=PRIORIDADES)
    p.add_argument("-o", "--ordenar", choices=CRITERIOS_ORDENACAO, default="id")
    p.set_defaults(func=cmd_listar)

    p = sub.add_parser("buscar", help="buscar tarefas por palavra-chave")
    p.add_argument("termo", help="texto procurado no título ou na descrição")
    p.add_argument("-o", "--ordenar", choices=CRITERIOS_ORDENACAO, default="id")
    p.set_defaults(func=cmd_buscar)

    p = sub.add_parser("editar", help="alterar campos de uma tarefa")
    p.add_argument("id", type=int)
    p.add_argument("-t", "--titulo")
    p.add_argument("-d", "--descricao")
    p.add_argument("-p", "--prioridade", choices=PRIORIDADES)
    prazo = p.add_mutually_exclusive_group()
    prazo.add_argument("--prazo", help="novo prazo no formato AAAA-MM-DD")
    prazo.add_argument("--sem-prazo", action="store_true", help="remover o prazo")
    p.set_defaults(func=cmd_editar)

    p = sub.add_parser("concluir", help="marcar uma tarefa como concluída")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_concluir)

    p = sub.add_parser("reabrir", help="voltar uma tarefa concluída para pendente")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_reabrir)

    p = sub.add_parser("remover", help="excluir uma tarefa")
    p.add_argument("id", type=int)
    p.add_argument("-y", "--sim", action="store_true", help="não pedir confirmação")
    p.set_defaults(func=cmd_remover)

    p = sub.add_parser("resumo", help="mostrar o progresso das tarefas")
    p.set_defaults(func=cmd_resumo)
    return parser


def cmd_adicionar(servico: TaskService, args, entrada) -> int:
    tarefa = servico.adicionar(
        args.titulo, descricao=args.descricao, prioridade=args.prioridade, prazo=args.prazo
    )
    print(f"Tarefa {tarefa.id} criada: {tarefa.titulo}")
    return SUCESSO


def cmd_listar(servico: TaskService, args, entrada) -> int:
    tarefas = servico.listar(
        status=args.status, prioridade=args.prioridade, ordenar_por=args.ordenar
    )
    print(formatar_tabela(tarefas, servico.hoje()))
    return SUCESSO


def cmd_buscar(servico: TaskService, args, entrada) -> int:
    print(formatar_tabela(servico.buscar(args.termo, args.ordenar), servico.hoje()))
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


def cmd_concluir(servico: TaskService, args, entrada) -> int:
    if servico.concluir(args.id):
        print(f"Tarefa {args.id} concluída.")
    else:
        print(f"Tarefa {args.id} já estava concluída.")
    return SUCESSO


def cmd_reabrir(servico: TaskService, args, entrada) -> int:
    if servico.reabrir(args.id):
        print(f"Tarefa {args.id} reaberta.")
    else:
        print(f"Tarefa {args.id} já estava pendente.")
    return SUCESSO


def cmd_remover(servico: TaskService, args, entrada) -> int:
    tarefa = servico.obter(args.id)
    if not args.sim:
        try:
            resposta = entrada(f'Remover a tarefa {tarefa.id} "{tarefa.titulo}"? [s/N] ')
        except EOFError:
            resposta = ""
        if resposta.strip().lower() not in ("s", "sim"):
            print("Remoção cancelada.")
            return SUCESSO
    servico.remover(args.id)
    print(f"Tarefa {args.id} removida.")
    return SUCESSO


def cmd_resumo(servico: TaskService, args, entrada) -> int:
    print(formatar_resumo(servico.resumo()))
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
    except ArquivoCorrompidoError as erro:
        print(f"Erro: o arquivo de dados está corrompido: {erro.caminho}", file=sys.stderr)
        print(f"Uma cópia foi salva em {erro.backup}", file=sys.stderr)
        return ERRO_DADOS
    except RepositorioError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return ERRO_DADOS
