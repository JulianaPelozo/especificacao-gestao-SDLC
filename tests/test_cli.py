import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from pathlib import Path

from taskflow import __version__
from taskflow.cli import main
from taskflow.repository import RepositorioJSON
from taskflow.services import TaskService

AGORA = datetime(2026, 11, 10, 12, 0)


class TestCliBasico(unittest.TestCase):
    def test_versao(self):
        saida = io.StringIO()
        with redirect_stdout(saida), self.assertRaises(SystemExit) as ctx:
            main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn(__version__, saida.getvalue())


class BaseCli(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.caminho = Path(self._tmp.name) / "tarefas.json"
        self.repo = RepositorioJSON(self.caminho)

    def tearDown(self):
        self._tmp.cleanup()

    def executar(self, *argv, respostas=()):
        """Executa a CLI e devolve (código, stdout, stderr)."""
        respostas = list(respostas)

        def entrada(pergunta):
            print(pergunta, end="")
            if not respostas:
                raise EOFError
            return respostas.pop(0)

        servico = TaskService(self.repo, relogio=lambda: AGORA)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            codigo = main(list(argv), servico=servico, entrada=entrada)
        return codigo, out.getvalue(), err.getvalue()


class TestAdicionar(BaseCli):
    def test_adicionar_com_todos_os_campos(self):
        codigo, out, _ = self.executar(
            "adicionar", "Estudar Git", "--descricao", "Cap. 3", "--prioridade", "alta",
            "--prazo", "2026-11-14",
        )
        self.assertEqual(codigo, 0)
        self.assertEqual(out.strip(), "Tarefa 1 criada: Estudar Git")
        [t] = self.repo.carregar()
        self.assertEqual((t.prioridade.value, t.prazo.isoformat()), ("alta", "2026-11-14"))

    def test_titulo_vazio(self):
        codigo, _, err = self.executar("adicionar", "   ")
        self.assertEqual(codigo, 1)
        self.assertEqual(err.strip(), "Erro: o título não pode ser vazio.")
        self.assertFalse(self.caminho.exists())

    def test_prazo_invalido(self):
        codigo, _, err = self.executar("adicionar", "Prova", "--prazo", "10/11/2026")
        self.assertEqual(codigo, 1)
        self.assertIn("prazo inválido", err)


if __name__ == "__main__":
    unittest.main()
