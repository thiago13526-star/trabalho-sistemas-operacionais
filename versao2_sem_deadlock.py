import threading
import time

N = 4
garfos = [threading.Lock() for _ in range(N)]
lock_log = threading.Lock()
refeicoes = [0] * N
em_execucao = True
inicio = time.time()


def log(msg):
  with lock_log:
    tempo = time.time() - inicio
    print(f"[{tempo:.2f}s] {msg}")


def filosofo(id_filosofo):
  esquerda = id_filosofo
  direita = (id_filosofo + 1) % N

  if esquerda < direita:
    primeiro = esquerda
    segundo = direita
  else:
    primeiro = direita
    segundo = esquerda

  while em_execucao:
    log(f"F{id_filosofo} pensando")
    time.sleep(0.1)
    if not em_execucao:
      break

    with garfos[primeiro]:
      log(f"F{id_filosofo} pegou garfo {primeiro}")
      with garfos[segundo]:
        log(f"F{id_filosofo} pegou garfo {segundo}")
        log(f"F{id_filosofo} comendo")
        time.sleep(0.1)
        refeicoes[id_filosofo] += 1

    log(f"F{id_filosofo} largou garfos")


threads = []
for i in range(N):
  t = threading.Thread(target=filosofo, args=(i,))
  threads.append(t)
  t.start()

time.sleep(10)
em_execucao = False

for t in threads:
  t.join()

resumo = ""
for i in range(N):
  resumo += f"F{i}={refeicoes[i]} "

print("\nRefeicoes por filosofo:", resumo.strip())
print(f"Total: {sum(refeicoes)} refeicoes em 10s")