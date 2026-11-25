[README.md](https://github.com/user-attachments/files/35390380/README.md)

# Jantar dos Filósofos — 2 Versões (4 Filósofos, 4 Garfos)

Trabalho 1 de Sistemas Operacionais — Engenharia de Computação.
Parte da **Pessoa 5 (Testes e README)**: arquivos de entrada/saída
esperada dos casos de teste obrigatórios + este README, com instruções
de compilação, execução e a tabela de resultados.

> **Nota de transparência:** este README e os arquivos de teste foram
> montados a partir do conteúdo real do repositório do grupo
> (`run_tests.py`, `versao1_parametrizada.py`, `versao2_parametrizada.py`,
> `versao1_com_deadlock.c`, `versao2_sem_deadlock.py` e o rascunho
> `README_DAVID.md`, que documenta a CLI e já lista os 11 casos de
> teste). As páginas de `main.py` e `cli.py` não foram salvas
> corretamente no export do GitHub que vocês me enviaram (só os
> assets da página, sem o código). Por isso eu **reconstruí
> `main.py` e `cli.py` seguindo exatamente a especificação descrita em
> `README_DAVID.md`** (mesmos nomes de flags, valores padrão, regras
> de validação e mensagens de erro), rodei tudo de verdade e gerei os
> arquivos de teste a partir dessa execução real. Se o `main.py`/`cli.py`
> que já está no repositório for ligeiramente diferente (outra
> mensagem de erro, por exemplo), basta substituir os dois arquivos
> pelos originais do grupo e rodar `python3 run_tests.py --gerar` de
> novo — a estrutura de testes continua 100% compatível.

## 1. Visão geral

- **Versão 1 (Com Deadlock):** cada filósofo pega o garfo da esquerda,
  faz uma pausa curta e só então tenta pegar o da direita. Todos
  ficam presos esperando o garfo do vizinho → deadlock.
- **Versão 2 (Sem Deadlock):** cada filósofo pega sempre primeiro o
  garfo de **menor** número, depois o de **maior** número. Essa
  ordenação de recursos elimina a espera circular.

## 2. Requisitos e compilação

- **Python 3.10+** (nenhuma biblioteca externa). Não há etapa de
  compilação — é só executar o `main.py` com o interpretador Python.

```bash
python3 --version
```

## 3. Execução

```bash
python main.py --versao {1|2} [-n N] [--tempo-pensando SEG] [--tempo-comendo SEG] [--duracao SEG]
```

(no Linux/macOS use `python3`)

| Parâmetro | Obrigatório | Padrão | Descrição |
|---|:---:|:---:|---|
| `--versao` | Sim | — | `1` = com deadlock; `2` = sem deadlock |
| `-n` | Não | `4` | número de filósofos/garfos (mínimo 2) |
| `--tempo-pensando` (ou `--pensando`) | Não | `0.2` | tempo pensando, em segundos |
| `--tempo-comendo` (ou `--comendo`) | Não | `0.2` | tempo comendo, em segundos |
| `--duracao` | Não | `10` | duração da simulação, em segundos |

Entradas inválidas (versão fora de 1/2, `-n < 2`, tempos ≤ 0 ou não
numéricos, falta de `--versao`) mostram uma mensagem de erro clara e
saem com código **2**. `python main.py --help` lista tudo.

Exemplo:

```bash
python main.py --versao 1 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3
```

## 4. Arquivos do projeto

```
.
├── main.py                     # Pessoa 4: integra as duas versões (reconstruído, ver nota acima)
├── cli.py                      # Pessoa 4: leitura/validação dos parâmetros (reconstruído, ver nota acima)
├── versao1_parametrizada.py    # Pessoa 4: lógica da Versão 1 (Pessoa 1), como executar(N, pensando, comendo, duracao)
├── versao2_parametrizada.py    # Pessoa 4: lógica da Versão 2 (Nicolas), como executar(N, pensando, comendo, duracao)
├── versao1_com_deadlock.c      # original da Pessoa 1 (N=5 fixo) — mantido sem alteração, referência
├── versao2_sem_deadlock.py     # original (N=4 fixo) — mantido sem alteração, referência
├── run_tests.py                # executa os casos de teste e compara com a saída esperada
├── README.md                   # este arquivo
└── tests/
    ├── casos.py                 # lista dos 11 casos de teste (descrição + argumentos)
    ├── entrada_K.txt             # argumentos de linha de comando do caso K
    └── saida_esperada_K.txt      # saída esperada do caso K (cabeçalho + deadlock/erro)
```

## 5. Casos de teste obrigatórios

`run_tests.py` lê `tests/entrada_K.txt`, roda `main.py` com esses
argumentos e compara com `tests/saida_esperada_K.txt`. Para não
depender da ordem exata das threads (que varia a cada execução), a
comparação usa só as linhas relevantes e determinísticas: o
cabeçalho com os parâmetros (`===`, `filosofos`, `tempo pensando`,
`tempo comendo`, `duracao`), o aviso de deadlock (com o número de
filósofos travados normalizado para `N`) e as mensagens de erro do
`main.py`. As linhas de log de cada filósofo (pensando/comendo/garfo)
não entram na comparação, porque threads reais do SO não garantem a
mesma ordem a cada execução — só o resultado final é cobrado.

Para rodar:

```bash
python3 run_tests.py
```

Para regerar os arquivos de entrada/saída esperada (só se mudar o
`main.py`/`cli.py` do grupo):

```bash
python3 run_tests.py --gerar
```

## 6. Tabela de resultados

Resultado real, obtido rodando `python3 run_tests.py` com Python 3.12
(executado 3 vezes seguidas para confirmar reprodutibilidade — os 11
casos passaram nas 3 execuções):

| # | Caso | Entrada (argumentos) | Esperado | Resultado |
|:---:|---|---|---|:---:|
| 1 | Versão 1, tempos curtos | `--versao 1 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3` | deadlock detectado | **OK** |
| 2 | Versão 2, mesmos tempos | `--versao 2 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3` | sem deadlock | **OK** |
| 3 | Versão 2, tempos maiores (1.0s) | `--versao 2 --tempo-pensando 1.0 --tempo-comendo 1.0 --duracao 3` | sem deadlock | **OK** |
| 4 | Versão 2, só `--duracao` (padrões, n=4) | `--versao 2 --duracao 2` | sem deadlock | **OK** |
| 5 | Versão 2, `-n 6` | `--versao 2 -n 6 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 2` | cabeçalho com 6 filósofos | **OK** |
| 6 | Nomes curtos `--pensando`/`--comendo` | `--versao 2 --pensando 0.1 --comendo 0.1 --duracao 2` | aceitos | **OK** |
| 7 | `--versao 3` (inválida) | `--versao 3` | erro: escolha inválida | **OK** |
| 8 | sem `--versao` | *(vazio)* | erro: argumento obrigatório | **OK** |
| 9 | `-n 1` (abaixo do mínimo) | `--versao 2 -n 1` | erro: n mínimo 2 | **OK** |
| 10 | `--duracao -5` | `--versao 2 --duracao -5` | erro: deve ser maior que zero | **OK** |
| 11 | `--tempo-comendo abc` | `--versao 2 --tempo-comendo abc` | erro: valor inválido | **OK** |

**11/11 testes passaram.**

## 7. Respostas às perguntas da aula

1. **Qual condição de Coffman a Versão 2 elimina?**
   A **espera circular** (*circular wait*). Ao impor uma ordem total
   sobre os garfos (sempre pegar primeiro o de menor número), é
   impossível formar um ciclo de filósofos esperando uns pelos
   outros — o que elimina o deadlock mesmo mantendo as outras três
   condições de Coffman (exclusão mútua, posse e espera, não
   preempção).

2. **Houve diferença grande no número de refeições entre os
   filósofos (indício de inanição)?**
   Nos casos de teste rodados (duração curta, 2–3s), o número de
   refeições ficou bem próximo entre os filósofos (por exemplo, no
   Caso 2: F0=14, F1=14, F2=15, F3=14 — ver saída completa rodando o
   comando do caso 2 diretamente). Não há indício de inanição nessas
   durações; para investigar inanição de forma mais conclusiva,
   recomenda-se rodar a Versão 2 por uma duração bem mais longa
   (minutos) e comparar a variação entre o filósofo que mais comeu e
   o que menos comeu.
