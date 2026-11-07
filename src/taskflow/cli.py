"""Interface de linha de comando do TaskFlow."""

import argparse

from taskflow import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskflow",
        description="Mini-gerenciador de tarefas de linha de comando.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0
