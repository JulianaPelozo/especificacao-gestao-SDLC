import unittest
from datetime import date

from taskflow.formatters import barra_progresso, formatar_resumo, formatar_tabela
from taskflow.models import Tarefa
from taskflow.services import Resumo


class TestFormatters(unittest.TestCase):
    def test_tabela_vazia(self):
        self.assertEqual(formatar_tabela([]), "Nenhuma tarefa encontrada.")

    def test_tabela_alinha_colunas_e_marca_atraso(self):
        tarefas = [
            Tarefa(id=1, titulo="Entregar relatório", prioridade="alta", prazo="2026-11-05"),
            Tarefa(id=10, titulo="Ler", prioridade="baixa"),
        ]
        linhas = formatar_tabela(tarefas, hoje=date(2026, 11, 10)).splitlines()
        self.assertTrue(linhas[0].startswith("ID  STATUS    PRIORIDADE  PRAZO"))
        self.assertIn("2026-11-05!", linhas[2])
        self.assertEqual(linhas[2].index("Entregar"), linhas[3].index("Ler"))
        self.assertIn("2 tarefa(s).", linhas[-1])

    def test_barra_progresso(self):
        self.assertEqual(barra_progresso(0), "░" * 20)
        self.assertEqual(barra_progresso(100), "█" * 20)
        self.assertEqual(barra_progresso(50).count("█"), 10)

    def test_resumo(self):
        texto = formatar_resumo(Resumo(total=4, pendentes=3, concluidas=1, atrasadas=1))
        self.assertIn("Concluídas:  1", texto)
        self.assertTrue(texto.endswith("25%"))


if __name__ == "__main__":
    unittest.main()
