#!/usr/bin/env python3
"""main.py - Pessoa 4: integracao das duas versoes (ambas em Python).

Reconstruido a partir da especificacao em README_DAVID.md (o arquivo
original nao foi salvo corretamente no export do GitHub). Le os
parametros via cli.py e chama executar(N, pensando, comendo, duracao)
de versao1_parametrizada.py ou versao2_parametrizada.py.

As linhas do cabecalho abaixo ("===", "filosofos", "tempo pensando",
"tempo comendo", "duracao") sao exatamente as que run_tests.py filtra
(PREFIXOS) para compor a saida esperada de cada caso de teste.
"""
from cli import parse_args
import versao1_parametrizada
import versao2_parametrizada


def main(argv=None):
    args = parse_args(argv)

    print("=== Jantar dos Filosofos ===")
    print(f"versao: {args.versao}")
    print(f"filosofos: {args.n}")
    print(f"tempo pensando: {args.pensando}")
    print(f"tempo comendo: {args.comendo}")
    print(f"duracao: {args.duracao}")
    print("=============================")

    if args.versao == 1:
        versao1_parametrizada.executar(args.n, args.pensando, args.comendo, args.duracao)
    else:
        versao2_parametrizada.executar(args.n, args.pensando, args.comendo, args.duracao)


if __name__ == "__main__":
    main()
