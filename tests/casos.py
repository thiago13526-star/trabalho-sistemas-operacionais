# (descricao, argumentos)
CASOS = [
 ("Versao 1 deve travar (deadlock)", "--versao 1 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3"),
 ("Versao 2 nao trava", "--versao 2 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 3"),
 ("Versao 2 com tempo de pensar longo (sem falso deadlock)", "--versao 2 --tempo-pensando 1.0 --tempo-comendo 0.1 --duracao 3"),
 ("Valores padrao (n=4) na versao 2", "--versao 2 --duracao 2"),
 ("n = 6 filosofos na versao 2", "--versao 2 -n 6 --tempo-pensando 0.1 --tempo-comendo 0.1 --duracao 2"),
 ("Nomes curtos dos parametros (--pensando/--comendo)", "--versao 2 --pensando 0.1 --comendo 0.1 --duracao 2"),
 ("Versao invalida", "--versao 3"),
 ("Falta o parametro obrigatorio --versao", "-n 4 --duracao 2"),
 ("n invalido (1 filosofo)", "--versao 2 -n 1"),
 ("Duracao negativa", "--versao 2 --duracao -5"),
 ("Tempo nao numerico", "--versao 1 --tempo-comendo abc"),
]
