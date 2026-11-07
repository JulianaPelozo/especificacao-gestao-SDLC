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


class TestListar(BaseServico):
    def setUp(self):
        super().setUp()
        self.servico.adicionar("Estudar Git", prioridade="alta")
        self.servico.adicionar("Ler artigo", prioridade="baixa")
        tarefas = self.repo.carregar()
        tarefas[1].concluir(AGORA)
        self.repo.salvar(tarefas)

    def test_lista_todas(self):
        self.assertEqual([t.id for t in self.servico.listar()], [1, 2])

    def test_filtra_por_status(self):
        self.assertEqual([t.id for t in self.servico.listar(status="pendente")], [1])

    def test_filtra_por_prioridade(self):
        self.assertEqual([t.id for t in self.servico.listar(prioridade="baixa")], [2])

    def test_filtros_combinados_sem_resultado(self):
        self.assertEqual(self.servico.listar(status="pendente", prioridade="baixa"), [])


class TestEditar(BaseServico):
    def setUp(self):
        super().setUp()
        self.servico.adicionar("Estudar Git", "cap. 3", "alta", "2026-11-14")

    def test_altera_apenas_campos_informados(self):
        t = self.servico.editar(1, prioridade="baixa")
        self.assertIs(t.prioridade, Prioridade.BAIXA)
        self.assertEqual(t.titulo, "Estudar Git")
        self.assertEqual(t.descricao, "cap. 3")
        self.assertEqual(self.repo.carregar()[0], t)

    def test_remove_prazo(self):
        self.assertIsNone(self.servico.editar(1, remover_prazo=True).prazo)

    def test_id_inexistente(self):
        with self.assertRaises(TarefaNaoEncontradaError):
            self.servico.editar(99, titulo="X")

    def test_valor_invalido_nao_altera_arquivo(self):
        antes = self.repo.caminho.read_text(encoding="utf-8")
        with self.assertRaises(ValidacaoError):
            self.servico.editar(1, titulo="Novo", prazo="amanhã")
        self.assertEqual(self.repo.caminho.read_text(encoding="utf-8"), antes)


class TestConcluirReabrir(BaseServico):
    def setUp(self):
        super().setUp()
        self.servico.adicionar("Estudar Git")

    def test_concluir_registra_data(self):
        self.assertTrue(self.servico.concluir(1))
        [t] = self.repo.carregar()
        self.assertIs(t.status, Status.CONCLUIDA)
        self.assertEqual(t.concluida_em, AGORA)

    def test_concluir_duas_vezes(self):
        self.servico.concluir(1)
        self.assertFalse(self.servico.concluir(1))

    def test_reabrir(self):
        self.servico.concluir(1)
        self.assertTrue(self.servico.reabrir(1))
        [t] = self.repo.carregar()
        self.assertIs(t.status, Status.PENDENTE)
        self.assertIsNone(t.concluida_em)
        self.assertFalse(self.servico.reabrir(1))

    def test_id_inexistente(self):
        with self.assertRaises(TarefaNaoEncontradaError):
            self.servico.concluir(42)


class TestRemover(BaseServico):
    def test_remove_e_nao_reutiliza_id(self):
        self.servico.adicionar("A")
        self.servico.adicionar("B")
        self.servico.remover(2)
        self.assertEqual([t.id for t in self.repo.carregar()], [1])
        self.assertEqual(self.servico.adicionar("C").id, 2)
        self.servico.remover(1)
        self.assertEqual(self.servico.adicionar("D").id, 3)

    def test_id_inexistente(self):
        with self.assertRaises(TarefaNaoEncontradaError):
            self.servico.remover(1)


class TestBuscarOrdenar(BaseServico):
    def setUp(self):
        super().setUp()
        self.servico.adicionar("Revisar Programação", prioridade="baixa", prazo="2026-11-20")
        self.servico.adicionar("Estudar", "capítulo sobre GIT", prioridade="alta")
        self.servico.adicionar("Prova", prioridade="media", prazo="2026-11-12")

    def test_busca_sem_acentos_e_maiusculas(self):
        self.assertEqual([t.id for t in self.servico.buscar("programacao")], [1])

    def test_busca_na_descricao(self):
        self.assertEqual([t.id for t in self.servico.buscar("git")], [2])

    def test_busca_sem_resultado(self):
        self.assertEqual(self.servico.buscar("inexistente"), [])

    def test_ordenar_por_prazo_sem_prazo_por_ultimo(self):
        self.assertEqual([t.id for t in self.servico.listar(ordenar_por="prazo")], [3, 1, 2])

    def test_ordenar_por_prioridade(self):
        self.assertEqual([t.id for t in self.servico.listar(ordenar_por="prioridade")], [2, 3, 1])


if __name__ == "__main__":
    unittest.main()
