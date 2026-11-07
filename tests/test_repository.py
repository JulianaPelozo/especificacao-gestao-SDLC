import json
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from taskflow.models import Prioridade, Tarefa
from taskflow.repository import ArquivoCorrompidoError, RepositorioJSON, caminho_padrao


class TestRepositorioJSON(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.caminho = self.dir / "sub" / "tarefas.json"
        self.repo = RepositorioJSON(self.caminho)

    def tearDown(self):
        self._tmp.cleanup()

    def test_arquivo_inexistente_retorna_lista_vazia(self):
        self.assertEqual(self.repo.carregar(), [])

    def test_salvar_e_recarregar(self):
        tarefas = [
            Tarefa(id=1, titulo="Estudar Git", prioridade=Prioridade.ALTA, prazo=date(2026, 11, 10)),
            Tarefa(id=2, titulo="Ler artigo"),
        ]
        self.repo.salvar(tarefas)
        recarregadas = RepositorioJSON(self.caminho).carregar()
        self.assertEqual(recarregadas, tarefas)

    def test_formato_do_arquivo(self):
        self.repo.salvar([Tarefa(id=1, titulo="Programação")])
        texto = self.caminho.read_text(encoding="utf-8")
        self.assertIn("Programação", texto)  # UTF-8 legível, sem \u escapes
        dados = json.loads(texto)
        self.assertEqual(dados["versao"], 1)
        self.assertEqual(len(dados["tarefas"]), 1)

    def test_nao_deixa_arquivos_temporarios(self):
        self.repo.salvar([Tarefa(id=1, titulo="X")])
        self.assertEqual([p.name for p in self.caminho.parent.iterdir()], ["tarefas.json"])

    def test_variavel_de_ambiente_define_caminho(self):
        with mock.patch.dict(os.environ, {"TASKFLOW_ARQUIVO": str(self.dir / "x.json")}):
            self.assertEqual(caminho_padrao(), self.dir / "x.json")

    def test_caminho_padrao_no_diretorio_do_usuario(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(caminho_padrao().name, "tarefas.json")
            self.assertEqual(caminho_padrao().parent.name, ".taskflow")

    def test_json_invalido_gera_erro_e_backup(self):
        self.caminho.parent.mkdir(parents=True)
        self.caminho.write_text("{abc", encoding="utf-8")
        with self.assertRaises(ArquivoCorrompidoError) as ctx:
            self.repo.carregar()
        self.assertEqual(ctx.exception.backup.read_text(encoding="utf-8"), "{abc")
        self.assertEqual(self.caminho.read_text(encoding="utf-8"), "{abc")

    def test_estrutura_invalida_gera_erro(self):
        self.caminho.parent.mkdir(parents=True)
        for conteudo in ('[]', '{"tarefas": [{"id": 1}]}', '{"tarefas": [{"id": 1, "titulo": ""}]}'):
            with self.subTest(conteudo=conteudo):
                self.caminho.write_text(conteudo, encoding="utf-8")
                with self.assertRaises(ArquivoCorrompidoError):
                    self.repo.carregar()


if __name__ == "__main__":
    unittest.main()
