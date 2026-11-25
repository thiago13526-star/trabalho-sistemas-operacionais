"""cli.py - Pessoa 4: leitura e validacao dos parametros de linha de comando.

Reconstruido a partir da especificacao em README_DAVID.md (o arquivo
original nao foi salvo corretamente no export do GitHub). Mantem os
mesmos nomes de flags, valores padrao e regras de validacao descritos
la, para que os 11 casos de teste documentados continuem valendo.
"""
import argparse


def _tempo_positivo(valor):
    try:
        f = float(valor)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"valor invalido: {valor!r} (deve ser um numero)")
    if f <= 0:
        raise argparse.ArgumentTypeError(
            f"valor invalido: {valor!r} (deve ser maior que zero)")
    return f


def _n_minimo_dois(valor):
    try:
        i = int(valor)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"valor invalido: {valor!r} (deve ser um numero inteiro)")
    if i < 2:
        raise argparse.ArgumentTypeError(
            f"-n deve ser no minimo 2 (recebido {i})")
    return i


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Jantar dos Filosofos - Versao 1 (com deadlock) e Versao 2 (sem deadlock)")
    parser.add_argument(
        "--versao", type=int, choices=[1, 2], required=True,
        help="1 = com deadlock, 2 = sem deadlock")
    parser.add_argument(
        "-n", type=_n_minimo_dois, default=4,
        help="numero de filosofos/garfos (minimo 2, padrao 4)")
    parser.add_argument(
        "--tempo-pensando", "--pensando", dest="pensando",
        type=_tempo_positivo, default=0.2,
        help="tempo pensando, em segundos (padrao 0.2)")
    parser.add_argument(
        "--tempo-comendo", "--comendo", dest="comendo",
        type=_tempo_positivo, default=0.2,
        help="tempo comendo, em segundos (padrao 0.2)")
    parser.add_argument(
        "--duracao", type=_tempo_positivo, default=10.0,
        help="duracao da simulacao, em segundos (padrao 10)")
    return parser.parse_args(argv)
