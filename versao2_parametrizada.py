"""Versao 2 - SEM DEADLOCK, com parametros (Pessoa 4).
Baseada na logica de versao2_sem_deadlock.py (Nicolas), que continua intacto.
Aqui o codigo virou a funcao executar(), que recebe N, tempos e duracao
em vez de usar valores fixos. A logica e a mesma.
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
      tempo = time.time() - inicio
      print(f"[{tempo:.2f}s] {msg}", flush=True)

  def filosofo(id_filosofo):
    esquerda = id_filosofo
    direita = (id_filosofo + 1) % N

    if esquerda < direita:
      primeiro = esquerda
      segundo = direita
    else:
      primeiro = direita
      segundo = esquerda

    while estado["em_execucao"]:
      log(f"F{id_filosofo} pensando")
      time.sleep(pensando)
      if not estado["em_execucao"]:
        break

      with garfos[primeiro]:
        log(f"F{id_filosofo} pegou garfo {primeiro}")
        with garfos[segundo]:
          log(f"F{id_filosofo} pegou garfo {segundo}")
          log(f"F{id_filosofo} comendo")
          time.sleep(comendo)
          refeicoes[id_filosofo] += 1

      log(f"F{id_filosofo} largou garfos")

  threads = []
  for i in range(N):
    t = threading.Thread(target=filosofo, args=(i,))
    threads.append(t)
    t.start()

  time.sleep(duracao)
  estado["em_execucao"] = False

  for t in threads:
    t.join()

  resumo = ""
  for i in range(N):
    resumo += f"F{i}={refeicoes[i]} "

  print("\nRefeicoes por filosofo:", resumo.strip())
  print(f"Total: {sum(refeicoes)} refeicoes em {duracao:.0f}s")
