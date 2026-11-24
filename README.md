# Jantar dos Filósofos — Versão 1 (Com Deadlock) e Versão 2 (Sem Deadlock)

Trabalho 1 de Sistemas Operacionais / Engenharia de Computação. Simulação
do problema clássico do Jantar dos Filósofos em Python, com duas versões
da política de alocação de garfos (recursos compartilhados):

- **Versão 1 — Com Deadlock:** cada filósofo pega sempre primeiro o garfo
  da sua esquerda e só depois tenta o da direita. Como todos pegam o
  garfo da esquerda ao mesmo tempo, forma-se uma **espera circular** e a
  simulação trava.
- **Versão 2 — Sem Deadlock:** os garfos são numerados de 0 a N-1 e cada
  filósofo pega sempre primeiro o garfo de **menor número** e depois o de
  maior número. Essa ordenação de recursos elimina a espera circular e
  todos os filósofos comem continuamente.

## 1. Requisitos

- Python 3.8 ou superior (usa apenas a biblioteca padrão: `threading`,
  `argparse`, `time`). Não há necessidade de instalar nenhuma dependência
  nem de compilar nada.

Verificar a versão instalada:

```bash
python3 --version
```

## 2. Execução

```bash
python3 jantar_filosofos.py --versao {1|2} [-n N] [--tempo-pensando T] [--tempo-comendo T] [--duracao T]
```

### Parâmetros de linha de comando

| Parâmetro | Obrigatório | Padrão | Descrição |
|---|---|---|---|
| `--versao` | Sim | — | `1` para a versão com deadlock, `2` para a versão sem deadlock |
| `-n` | Não | `4` | Número de filósofos e de garfos |
| `--tempo-pensando` | Não | `0.2` | Tempo médio (segundos) que cada filósofo passa pensando |
| `--tempo-comendo` | Não | `0.2` | Tempo médio (segundos) que cada filósofo passa comendo |
| `--duracao` | Não | `10` | Duração total da simulação, em segundos |

### Exemplos

```bash
# Versão 1 (com deadlock), 4 filósofos, 10 segundos
python3 jantar_filosofos.py --versao 1 -n 4 --duracao 10

# Versão 2 (sem deadlock), 4 filósofos, 10 segundos
python3 jantar_filosofos.py --versao 2 -n 4 --duracao 10

# Versão 2 com 6 filósofos e tempos customizados
python3 jantar_filosofos.py --versao 2 -n 6 --tempo-pensando 0.1 --tempo-comendo 0.3 --duracao 15
```

## 3. Saída do programa

Cada linha de log é impressa no formato `[tempo_decorrido]s mensagem`,
por exemplo:

```
[0.41s] F0 esperando garfo 1...
```

Ao final da simulação (ou ao detectar deadlock), o programa imprime um
resumo com o número de refeições de cada filósofo:

```
Refeicoes por filosofo: F0=25 F1=24 F2=25 F3=24
Total: 98 refeicoes em 5s
```

Na Versão 1, se algum filósofo continuar bloqueado após o tempo de
`--duracao`, o programa imprime explicitamente:

```
DEADLOCK DETECTADO: 4 filosofo(s) ainda bloqueado(s) apos 3s
```

## 4. Casos de teste

Os arquivos de entrada e saída esperada de cada caso estão na pasta
`testes/`. Cada subpasta contém:

- `entrada.txt` — o comando usado para rodar o teste;
- `saida_esperada.txt` — o padrão de comportamento esperado (critério de
  aprovação) e um exemplo real de saída;
- `saida_obtida.txt` — a saída completa realmente produzida pelo
  programa nessa execução, usada para comparação.

> **Observação:** como a simulação usa threads concorrentes, os
> timestamps exatos e a ordem de intercalação das linhas variam a cada
> execução. Por isso a "saída esperada" descreve o **padrão** de
> comportamento (sequência de eventos, ausência/presença de deadlock,
> número de refeições) em vez de exigir uma saída idêntica byte a byte.

| Caso | Versão | N | Duração | O que testa | Resultado obtido |
|---|---|---|---|---|---|
| 1 | 1 (com deadlock) | 4 | 3s | O programa trava e reporta o deadlock corretamente | ✅ 0 refeições, deadlock detectado |
| 2 | 2 (sem deadlock) | 4 | 5s | Os filósofos comem continuamente, sem travar | ✅ 98 refeições, sem deadlock |
| 3 | 2 (sem deadlock) | 6 | 5s | O parâmetro `-n` altera corretamente o número de filósofos | ✅ 147 refeições (6 filósofos), sem deadlock |

Para rodar os testes manualmente:

```bash
cd testes/caso1_versao1_deadlock && python3 ../../jantar_filosofos.py --versao 1 -n 4 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3
cd testes/caso2_versao2_sem_deadlock && python3 ../../jantar_filosofos.py --versao 2 -n 4 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 5
cd testes/caso3_versao2_n6 && python3 ../../jantar_filosofos.py --versao 2 -n 6 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 5
```

## 5. Perguntas da aula

1. **Qual condição de Coffman a Versão 2 elimina?**
   A **espera circular** (circular wait). Ao impor uma ordem total sobre
   os garfos — cada filósofo pega sempre primeiro o de menor número —
   torna-se impossível formar um ciclo de filósofos esperando uns pelos
   garfos dos outros.

2. **Houve diferença grande no número de refeições entre os filósofos
   (indício de inanição/starvation)?**
   Não. Nos testes realizados (ver tabela acima), a diferença entre o
   filósofo que mais comeu e o que menos comeu ficou em no máximo 1
   refeição, o que não caracteriza inanição.

## 6. Estrutura do repositório

```
.
├── jantar_filosofos.py
├── README.md
└── testes/
    ├── caso1_versao1_deadlock/
    │   ├── entrada.txt
    │   ├── saida_esperada.txt
    │   └── saida_obtida.txt
    ├── caso2_versao2_sem_deadlock/
    │   ├── entrada.txt
    │   ├── saida_esperada.txt
    │   └── saida_obtida.txt
    └── caso3_versao2_n6/
        ├── entrada.txt
        ├── saida_esperada.txt
        └── saida_obtida.txt
```
