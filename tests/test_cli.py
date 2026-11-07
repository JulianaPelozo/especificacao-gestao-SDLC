import io
import unittest
from contextlib import redirect_stdout

from taskflow import __version__
from taskflow.cli import main


class TestCliBasico(unittest.TestCase):
    def test_versao(self):
        saida = io.StringIO()
        with redirect_stdout(saida), self.assertRaises(SystemExit) as ctx:
            main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn(__version__, saida.getvalue())


if __name__ == "__main__":
    unittest.main()
