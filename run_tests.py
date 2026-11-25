"""Executa os casos de teste: le tests/entrada_K.txt e compara com tests/saida_esperada_K.txt.
Uso: python3 run_tests.py          (executa e compara)
     python3 run_tests.py --gerar  (regrava entrada/saida esperada - so para o autor)"""
import re, subprocess, sys, shlex
from pathlib import Path
sys.path.insert(0, "tests")
from casos import CASOS

T = Path("tests")
PREFIXOS = ("===", "filosofos", "tempo", "duracao", "main.py: error")

def saida_relevante(args):
    r = subprocess.run([sys.executable, "main.py", *shlex.split(args)],
                       capture_output=True, text=True)
    linhas = []
    for l in (r.stdout + r.stderr).splitlines():
        if "DEADLOCK DETECTADO" in l:
            l = re.sub(r"^\[[\d.]+s\] ", "", l)
            l = re.sub(r"\d+ filosofo", "N filosofo", l)
            linhas.append(l)
        elif l.startswith(PREFIXOS):
            linhas.append(l)
    return "\n".join(linhas) + "\n"

if "--gerar" in sys.argv:
    for k, (desc, args) in enumerate(CASOS, 1):
        (T / f"entrada_{k}.txt").write_text(args + "\n")
        (T / f"saida_esperada_{k}.txt").write_text(f"# {desc}\n" + saida_relevante(args))
    print("arquivos gerados"); sys.exit()

ok = 0
for k in range(1, len(CASOS) + 1):
    args = (T / f"entrada_{k}.txt").read_text().strip()
    esperado = (T / f"saida_esperada_{k}.txt").read_text().split("\n", 1)[1]
    obtido = saida_relevante(args)
    passou = esperado == obtido
    ok += passou
    print(f"Teste {k}: {'OK  ' if passou else 'FALHOU'} | {CASOS[k-1][0]}")
    if not passou:
        print("  esperado:\n" + esperado + "  obtido:\n" + obtido)
print(f"\n{ok}/{len(CASOS)} testes passaram")
sys.exit(0 if ok == len(CASOS) else 1)