"""Versao 1 - COM DEADLOCK, com parametros (Pessoa 4).
Baseada na logica de versao1_com_deadlock.c (Pessoa 1), que continua intacto.
Cada filosofo pega primeiro o garfo da esquerda e depois o da direita; com uma
pequena pausa entre os dois, todos ficam segurando um garfo esperando o outro
(espera circular = deadlock).
A funcao executar() recebe N, tempos e duracao em vez de valores fixos.
"""
import threading
import time


def executar(N, pensando, comendo, duracao):
    garfos = [threading.Lock() for _ in range(N)]
    lock_log = threading.Lock()
    refeicoes = [0] * N
    estado = {"em_execucao": True}
    inicio = time.time()

    def log(msg):
        with lock_log:
            print(f"[{time.time() - inicio:.2f}s] {msg}", flush=True)

    def filosofo(i):
        esq = i
        dir_ = (i + 1) % N

        while estado["em_execucao"]:
            log(f"F{i} pensando")
            time.sleep(pensando)
            if not estado["em_execucao"]:
                break

            garfos[esq].acquire()
            log(f"F{i} pegou garfo {esq}")
            time.sleep(0.3)  # pausa curta para forcar o impasse

            log(f"F{i} espera o garfo {dir_}...")
            garfos[dir_].acquire()  # deadlock acontece aqui
            log(f"F{i} pegou garfo {dir_}")

            log(f"F{i} comendo")
            refeicoes[i] += 1
            time.sleep(comendo)

            garfos[dir_].release()
            garfos[esq].release()
            log(f"F{i} largou garfos")

    # daemon=True: threads bloqueadas pelo deadlock nao impedem o programa de encerrar
    threads = [threading.Thread(target=filosofo, args=(i,), daemon=True) for i in range(N)]
    for t in threads:
        t.start()

    time.sleep(duracao)
    estado["em_execucao"] = False

    # da tempo para quem so esta dormindo terminar; quem sobrar esta bloqueado
    prazo = time.time() + pensando + comendo + 0.6
    for t in threads:
        t.join(timeout=max(0.0, prazo - time.time()))

    travadas = sum(1 for t in threads if t.is_alive())
    if travadas > 0:
        log(f"DEADLOCK DETECTADO: {travadas} filosofo(s) ainda bloqueado(s) apos {duracao:.0f}s")

    print("\nRefeicoes por filosofo:", " ".join(f"F{i}={refeicoes[i]}" for i in range(N)))
    print(f"Total: {sum(refeicoes)} refeicoes em {duracao:.0f}s")