"""Pessoa 4 - Parametros e Entrada (CLI).

Le e valida os parametros de linha de comando do Jantar dos Filosofos.
Aceita os nomes longos (--tempo-pensando) e os curtos (--pensando).
"""
import argparse


def _numero(tipo, nome):
    def conv(texto):
        try:
            v = tipo(texto)
        except ValueError:
            raise argparse.ArgumentTypeError(f"'{texto}' nao e um valor valido para {nome}")
        if v <= 0:
            raise argparse.ArgumentTypeError(f"{nome} deve ser maior que zero (recebido: {texto})")
        return v
    return conv


def _versao(texto):
    # mensagem propria, para nao depender do texto do argparse (muda entre versoes do Python)
    if texto not in ("1", "2"):
        raise argparse.ArgumentTypeError(f"versao deve ser 1 ou 2 (recebido: {texto})")
    return int(texto)


def ler_parametros(argv=None):
    p = argparse.ArgumentParser(
        prog="main.py",
        description="Jantar dos Filosofos - versao 1 (com deadlock) e versao 2 (sem deadlock).",
        epilog="Exemplo: python3 main.py --versao 2 -n 4 --tempo-pensando 0.2 --tempo-comendo 0.2 --duracao 10")
    p.add_argument("--versao", type=_versao, required=True, metavar="{1,2}",
                   help="1 = com deadlock; 2 = sem deadlock (ordenacao de recursos)")
    p.add_argument("-n", type=_numero(int, "-n"), default=4, metavar="N",
                   help="numero de filosofos/garfos (padrao: 4; minimo: 2)")
    p.add_argument("--tempo-pensando", "--pensando", dest="tempo_pensando",
                   type=_numero(float, "--tempo-pensando"), default=0.2, metavar="SEG",
                   help="tempo pensando, em segundos (padrao: 0.2)")
    p.add_argument("--tempo-comendo", "--comendo", dest="tempo_comendo",
                   type=_numero(float, "--tempo-comendo"), default=0.2, metavar="SEG",
                   help="tempo comendo, em segundos (padrao: 0.2)")
    p.add_argument("--duracao", type=_numero(float, "--duracao"), default=10.0, metavar="SEG",
                   help="duracao da simulacao, em segundos (padrao: 10)")
    args = p.parse_args(argv)
    if args.n < 2:
        p.error("-n deve ser pelo menos 2 (com 1 filosofo nao ha dois garfos)")
    return args


def descrever(a):
    nome = "Versao 1 (COM deadlock)" if a.versao == 1 else "Versao 2 (SEM deadlock)"
    return (f"=== Jantar dos Filosofos - {nome} ===\n"
            f"filosofos/garfos : {a.n}\n"
            f"tempo pensando   : {a.tempo_pensando}s\n"
            f"tempo comendo    : {a.tempo_comendo}s\n"
            f"duracao          : {a.duracao}s")
