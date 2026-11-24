#!/usr/bin/env python3
"""
Jantar dos Filosofos - Sistemas Operacionais / Engenharia de Computacao
Trabalho 1 - Versao 1 (Com Deadlock) e Versao 2 (Sem Deadlock)

Uso:
    python3 jantar_filosofos.py --versao 1 -n 4 --tempo-pensando 0.2 --tempo-comendo 0.2 --duracao 10
    python3 jantar_filosofos.py --versao 2 -n 4 --tempo-pensando 0.2 --tempo-comendo 0.2 --duracao 10
"""

import argparse
import threading
import time

lock_log = threading.Lock()
inicio = time.time()


def log(msg):
    with lock_log:
        tempo = time.time() - inicio
        print(f"[{tempo:.2f}s] {msg}")


def filosofo_v1(id_filosofo, N, garfos, tempo_pensando, tempo_comendo, refeicoes, rodando, barreira):
    """Versao 1 - COM DEADLOCK.

    Cada filosofo pega sempre primeiro o garfo da esquerda (seu proprio
    indice) e depois tenta pegar o garfo da direita. Uma barreira sincroniza
    os filosofos antes de pegarem o garfo da esquerda, garantindo que todos
    fiquem segurando um garfo e esperando o proximo -> espera circular
    (deadlock) logo na primeira rodada.
    """
    esquerda = id_filosofo
    direita = (id_filosofo + 1) % N

    while rodando.is_set():
        log(f"F{id_filosofo} pensando")
        time.sleep(tempo_pensando)
        if not rodando.is_set():
            break

        try:
            barreira.wait()
        except threading.BrokenBarrierError:
            break

        garfos[esquerda].acquire()
        log(f"F{id_filosofo} pegou garfo {esquerda}")

        time.sleep(0.3)  # pausa curta para forcar o impasse

        log(f"F{id_filosofo} esperando garfo {direita}...")
        garfos[direita].acquire()  # deadlock acontece aqui
        log(f"F{id_filosofo} pegou garfo {direita}")

        log(f"F{id_filosofo} comendo")
        time.sleep(tempo_comendo)
        refeicoes[id_filosofo] += 1

        garfos[direita].release()
        garfos[esquerda].release()
        log(f"F{id_filosofo} largou garfos")


def filosofo_v2(id_filosofo, N, garfos, tempo_pensando, tempo_comendo, refeicoes, rodando):
    """Versao 2 - SEM DEADLOCK.

    Os garfos sao numerados de 0 a N-1 e cada filosofo pega sempre primeiro
    o garfo de menor numero e depois o de maior numero (ordenacao de
    recursos), o que elimina a condicao de espera circular.
    """
    esquerda = id_filosofo
    direita = (id_filosofo + 1) % N
    primeiro, segundo = (esquerda, direita) if esquerda < direita else (direita, esquerda)

    while rodando.is_set():
        log(f"F{id_filosofo} pensando")
        time.sleep(tempo_pensando)
        if not rodando.is_set():
            break

        with garfos[primeiro]:
            log(f"F{id_filosofo} pegou garfo {primeiro}")
            with garfos[segundo]:
                log(f"F{id_filosofo} pegou garfo {segundo}")
                log(f"F{id_filosofo} comendo")
                time.sleep(tempo_comendo)
                refeicoes[id_filosofo] += 1

        log(f"F{id_filosofo} largou garfos")


def main():
    parser = argparse.ArgumentParser(description="Simulacao do Jantar dos Filosofos")
    parser.add_argument("--versao", type=int, choices=[1, 2], required=True,
                         help="1 = com deadlock, 2 = sem deadlock")
    parser.add_argument("-n", type=int, default=4,
                         help="numero de filosofos/garfos (padrao: 4)")
    parser.add_argument("--tempo-pensando", type=float, default=0.2,
                         help="tempo medio pensando, em segundos (padrao: 0.2)")
    parser.add_argument("--tempo-comendo", type=float, default=0.2,
                         help="tempo medio comendo, em segundos (padrao: 0.2)")
    parser.add_argument("--duracao", type=float, default=10,
                         help="duracao da simulacao, em segundos (padrao: 10)")
    args = parser.parse_args()

    N = args.n
    garfos = [threading.Lock() for _ in range(N)]
    refeicoes = [0] * N
    rodando = threading.Event()
    rodando.set()

    threads = []
    if args.versao == 1:
        barreira = threading.Barrier(N)
        for i in range(N):
            t = threading.Thread(
                target=filosofo_v1,
                args=(i, N, garfos, args.tempo_pensando, args.tempo_comendo, refeicoes, rodando, barreira),
                daemon=True,
            )
            threads.append(t)
            t.start()
    else:
        for i in range(N):
            t = threading.Thread(
                target=filosofo_v2,
                args=(i, N, garfos, args.tempo_pensando, args.tempo_comendo, refeicoes, rodando),
                daemon=True,
            )
            threads.append(t)
            t.start()

    time.sleep(args.duracao)
    rodando.clear()

    if args.versao == 1:
        # as threads da versao 1 ficam bloqueadas em acquire() e nao
        # percebem o sinal de parada -- isso e esperado em um deadlock real
        if 'barreira' in locals():
            barreira.abort()

    for t in threads:
        t.join(timeout=0.2)

    travadas = sum(1 for t in threads if t.is_alive())
    if travadas > 0:
        log(f"DEADLOCK DETECTADO: {travadas} filosofo(s) ainda bloqueado(s) apos {args.duracao:.0f}s")

    resumo = " ".join(f"F{i}={refeicoes[i]}" for i in range(N))
    print(f"\nRefeicoes por filosofo: {resumo}")
    print(f"Total: {sum(refeicoes)} refeicoes em {args.duracao:.0f}s")


if __name__ == "__main__":
    main()
