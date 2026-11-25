#!/usr/bin/env python3
"""Pessoa 4 - Parametros e Entrada (CLI) + integracao das duas versoes.

Le e valida os parametros (cli.py) e executa:
  --versao 1 -> versao1_parametrizada.py
  --versao 2 -> versao2_parametrizada.py
"""
from cli import ler_parametros, descrever


def main():
    a = ler_parametros()
    print(descrever(a), flush=True)
    if a.versao == 1:
        import versao1_parametrizada as versao
    else:
        import versao2_parametrizada as versao
    versao.executar(a.n, a.tempo_pensando, a.tempo_comendo, a.duracao)


if __name__ == "__main__":
    main()
