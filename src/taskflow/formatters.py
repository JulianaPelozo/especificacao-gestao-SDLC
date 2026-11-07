"""Formatação de saída em texto para o terminal."""

from datetime import date
from typing import List, Optional

from taskflow.models import Tarefa

LARGURA_BARRA = 20


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


def barra_progresso(percentual: int, largura: int = LARGURA_BARRA) -> str:
    cheios = round(largura * percentual / 100)
    return "█" * cheios + "░" * (largura - cheios)


def formatar_resumo(resumo) -> str:
    return "\n".join(
        [
            "Resumo das tarefas",
            "------------------",
            f"Total:       {resumo.total}",
            f"Pendentes:   {resumo.pendentes}",
            f"Concluídas:  {resumo.concluidas}",
            f"Atrasadas:   {resumo.atrasadas}",
            "",
            f"Progresso: [{barra_progresso(resumo.percentual)}] {resumo.percentual}%",
        ]
    )
