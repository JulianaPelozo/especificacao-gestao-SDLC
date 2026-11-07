import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

from taskflow.models import Prioridade, Status, ValidacaoError
from taskflow.repository import RepositorioJSON
from taskflow.services import TarefaNaoEncontradaError, TaskService

AGORA = datetime(2026, 11, 10, 12, 0)


class BaseServico(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = RepositorioJSON(Path(self._tmp.name) / "tarefas.json")
        self.servico = TaskService(self.repo, relogio=lambda: AGORA)

    def tearDown(self):
        self._tmp.cleanup()


class TestAdicionar(BaseServico):
    def test_ids_sequenciais(self):
        a = self.servico.adicionar("A")
        b = self.servico.adicionar("B")
        self.assertEqual((a.id, b.id), (1, 2))

    def test_persiste_campos(self):
        self.servico.adicionar("Estudar Git", "cap. 3", "alta", "2026-11-14")
        [salva] = self.repo.carregar()
        self.assertEqual(salva.titulo, "Estudar Git")
        self.assertIs(salva.prioridade, Prioridade.ALTA)
        self.assertEqual(salva.prazo, date(2026, 11, 14))
        self.assertEqual(salva.criada_em, AGORA)

    def test_titulo_invalido_nao_grava(self):
        with self.assertRaises(ValidacaoError):
            self.servico.adicionar("  ")
        self.assertFalse(self.repo.caminho.exists())


if __name__ == "__main__":
    unittest.main()
