import unittest
from datetime import date, datetime

from taskflow.models import Prioridade, Status, Tarefa, ValidacaoError


class TestValidacoes(unittest.TestCase):
    def test_titulo_vazio_e_rejeitado(self):
        for titulo in ("", "   ", None):
            with self.subTest(titulo=titulo), self.assertRaises(ValidacaoError):
                Tarefa(id=1, titulo=titulo)

    def test_titulo_muito_longo_e_rejeitado(self):
        with self.assertRaises(ValidacaoError):
            Tarefa(id=1, titulo="x" * 121)

    def test_titulo_e_descricao_sao_aparados(self):
        t = Tarefa(id=1, titulo="  Estudar Git  ", descricao="  cap. 3 ")
        self.assertEqual(t.titulo, "Estudar Git")
        self.assertEqual(t.descricao, "cap. 3")

    def test_prioridade_invalida_e_rejeitada(self):
        with self.assertRaises(ValidacaoError):
            Tarefa(id=1, titulo="X", prioridade="urgente")

    def test_prioridade_aceita_texto(self):
        self.assertIs(Tarefa(id=1, titulo="X", prioridade="ALTA").prioridade, Prioridade.ALTA)

    def test_prazo_invalido_e_rejeitado(self):
        with self.assertRaises(ValidacaoError):
            Tarefa(id=1, titulo="X", prazo="10/11/2026")

    def test_prazo_texto_e_convertido(self):
        self.assertEqual(Tarefa(id=1, titulo="X", prazo="2026-11-14").prazo, date(2026, 11, 14))

    def test_valores_padrao(self):
        t = Tarefa(id=1, titulo="X")
        self.assertIs(t.prioridade, Prioridade.MEDIA)
        self.assertIs(t.status, Status.PENDENTE)
        self.assertIsNone(t.prazo)


class TestComportamento(unittest.TestCase):
    def test_concluir_e_reabrir(self):
        t = Tarefa(id=1, titulo="X")
        agora = datetime(2026, 11, 8, 10, 30)
        self.assertTrue(t.concluir(agora))
        self.assertIs(t.status, Status.CONCLUIDA)
        self.assertEqual(t.concluida_em, agora)
        self.assertFalse(t.concluir(agora))
        self.assertTrue(t.reabrir())
        self.assertIs(t.status, Status.PENDENTE)
        self.assertIsNone(t.concluida_em)
        self.assertFalse(t.reabrir())

    def test_esta_atrasada(self):
        hoje = date(2026, 11, 10)
        self.assertTrue(Tarefa(id=1, titulo="X", prazo="2026-11-09").esta_atrasada(hoje))
        self.assertFalse(Tarefa(id=2, titulo="X", prazo="2026-11-10").esta_atrasada(hoje))
        self.assertFalse(Tarefa(id=3, titulo="X").esta_atrasada(hoje))
        concluida = Tarefa(id=4, titulo="X", prazo="2026-11-01")
        concluida.concluir()
        self.assertFalse(concluida.esta_atrasada(hoje))

    def test_peso_da_prioridade(self):
        self.assertLess(Prioridade.BAIXA.peso, Prioridade.MEDIA.peso)
        self.assertLess(Prioridade.MEDIA.peso, Prioridade.ALTA.peso)


class TestSerializacao(unittest.TestCase):
    def test_ida_e_volta_sem_perda(self):
        original = Tarefa(
            id=7,
            titulo="Revisar Programação",
            descricao="lista 2",
            prioridade=Prioridade.ALTA,
            prazo=date(2026, 11, 14),
            criada_em=datetime(2026, 11, 7, 20, 0),
        )
        original.concluir(datetime(2026, 11, 8, 9, 0))
        self.assertEqual(Tarefa.from_dict(original.to_dict()), original)

    def test_to_dict_usa_tipos_json(self):
        dados = Tarefa(id=1, titulo="X", criada_em=datetime(2026, 11, 7, 20, 0)).to_dict()
        self.assertEqual(dados["prioridade"], "media")
        self.assertIsNone(dados["prazo"])
        self.assertEqual(dados["criada_em"], "2026-11-07T20:00:00")


if __name__ == "__main__":
    unittest.main()
