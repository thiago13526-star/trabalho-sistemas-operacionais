"""Casos de teste obrigatorios do Jantar dos Filosofos.

Cada item e uma tupla (descricao, argumentos_de_linha_de_comando).
Esta lista reflete a tabela de 11 casos documentada em README_DAVID.md
(secao "Testes"), que e a referencia oficial combinada pela equipe.
"""

CASOS = [
    ("Versao 1 com tempos curtos -> deadlock detectado",
     "--versao 1 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3"),

    ("Versao 2 com os mesmos tempos -> sem deadlock",
     "--versao 2 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3"),

    ("Versao 2 com tempos maiores (1.0s) -> sem deadlock",
     "--versao 2 --tempo-pensando 1.0 --tempo-comendo 1.0 --duracao 3"),

    ("Versao 2 so com --duracao, resto no padrao (n=4) -> sem deadlock",
     "--versao 2 --duracao 2"),

    ("Versao 2 com -n 6 -> cabecalho mostra 6 filosofos",
     "--versao 2 -n 6 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 2"),

    ("Nomes curtos --pensando/--comendo sao aceitos",
     "--versao 2 --pensando 0.1 --comendo 0.1 --duracao 2"),

    ("Versao invalida (--versao 3) -> erro de escolha invalida",
     "--versao 3"),

    ("Sem --versao -> erro de argumento obrigatorio",
     ""),

    ("-n abaixo do minimo (-n 1) -> erro: minimo 2",
     "--versao 2 -n 1"),

    ("--duracao negativa -> erro: deve ser maior que zero",
     "--versao 2 --duracao -5"),

    ("--tempo-comendo nao numerico -> erro: valor invalido",
     "--versao 2 --tempo-comendo abc"),
]
