# Pessoa 4 — Parâmetros e Entrada (CLI) — texto para juntar ao README do grupo

## Como executar
Requisito: **Python 3.10+** (sem bibliotecas externas; não precisa compilar). Funciona em Windows, Linux e macOS.

```bash
python main.py --versao 1|2 [-n N] [--tempo-pensando SEG] [--tempo-comendo SEG] [--duracao SEG]
```
(no Linux/macOS use `python3`)

| Parâmetro | Obrigatório | Padrão | Descrição |
|---|---|---|---|
| `--versao` | sim | — | `1` = com deadlock; `2` = sem deadlock |
| `-n` | não | 4 | número de filósofos/garfos (mínimo 2) |
| `--tempo-pensando` (ou `--pensando`) | não | 0.2 | tempo pensando, em segundos |
| `--tempo-comendo` (ou `--comendo`) | não | 0.2 | tempo comendo, em segundos |
| `--duracao` | não | 10 | duração da simulação, em segundos |

Entradas inválidas (versão fora de 1/2, `-n < 2`, tempos ≤ 0 ou não numéricos, falta de `--versao`)
mostram mensagem de erro clara e saem com código 2. `python main.py --help` lista tudo.

## Arquivos
- `cli.py`, `main.py` — Pessoa 4: leitura/validação dos parâmetros e integração das versões.
- `versao1_parametrizada.py` e `versao2_parametrizada.py` — Pessoa 4: a mesma lógica das Versões 1 (Pessoa 1) e
  2 (Nicolas), reescritas como `executar(N, pensando, comendo, duracao)` para receber os parâmetros da CLI.
  Os arquivos originais `versao1_com_deadlock.c` e `versao2_sem_deadlock.py` **não foram alterados**.
- `run_tests.py`, `tests/` — testes.

## Testes
`python run_tests.py` lê `tests/entrada_K.txt` e compara com `tests/saida_esperada_K.txt`
(cabeçalho com os parâmetros, aviso de deadlock e mensagens de erro).

| # | Entrada | Esperado | Resultado |
|---|---|---|---|
| 1 | `--versao 1 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3` | deadlock detectado | OK |
| 2 | `--versao 2 ...` (mesmos tempos) | sem deadlock | OK |
| 3 | `--versao 2 --tempo-pensando 1.0 ...` | sem deadlock | OK |
| 4 | `--versao 2 --duracao 2` (padrões, n=4) | sem deadlock | OK |
| 5 | `--versao 2 -n 6 ...` | cabeçalho com 6 filósofos | OK |
| 6 | `--pensando`/`--comendo` (nomes curtos) | aceitos | OK |
| 7 | `--versao 3` | erro: escolha inválida | OK |
| 8 | sem `--versao` | erro: argumento obrigatório | OK |
| 9 | `--versao 2 -n 1` | erro: n mínimo 2 | OK |
| 10 | `--duracao -5` | erro: deve ser maior que zero | OK |
| 11 | `--tempo-comendo abc` | erro: valor inválido | OK |

## Contribuição da Pessoa 4
`cli.py` (parâmetros e validação), `main.py` (integração das duas versões (ambas em Python)), `run_tests.py` e `tests/`.
