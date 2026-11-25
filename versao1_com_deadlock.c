#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#define N 5

pthread_mutex_t garfo[N];
pthread_mutex_t mutex_log = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex_refeicoes = PTHREAD_MUTEX_INITIALIZER;

int refeicoes[N] = {0};
struct timespec inicio_execucao;

double tempo_decorrido() {
    struct timespec agora;
    clock_gettime(CLOCK_MONOTONIC, &agora);
    return (agora.tv_sec - inicio_execucao.tv_sec) +
           (agora.tv_nsec - inicio_execucao.tv_nsec) / 1e9;
}

void log_msg(const char *msg, int a, int b) {
    pthread_mutex_lock(&mutex_log);
    double t = tempo_decorrido();
    if (b >= 0) {
        printf("[%.2fs] ", t);
        printf(msg, a, b);
    } else if (a >= 0) {
        printf("[%.2fs] ", t);
        printf(msg, a);
    } else {
        printf("[%.2fs] %s\n", t, msg);
    }
    fflush(stdout);
    pthread_mutex_unlock(&mutex_log);
}

void registrar_refeicao(int i) {
    pthread_mutex_lock(&mutex_refeicoes);
    refeicoes[i]++;
    pthread_mutex_unlock(&mutex_refeicoes);
}

void imprimir_resumo() {
    int total = 0;
    pthread_mutex_lock(&mutex_refeicoes);
    pthread_mutex_lock(&mutex_log);

    printf("\nRefeicoes por filosofo:");
    for (int i = 0; i < N; i++) {
        printf(" F%d=%d", i, refeicoes[i]);
        total += refeicoes[i];
    }
    printf("\nTotal: %d refeicoes em %.2fs\n", total, tempo_decorrido());
    fflush(stdout);

    pthread_mutex_unlock(&mutex_log);
    pthread_mutex_unlock(&mutex_refeicoes);
}

void *filosofo(void *arg) {
    int i = (long long)arg;
    int esq = i;
    int dir = (i + 1) % N;

    pthread_mutex_lock(&garfo[esq]);
    log_msg("Filosofo %d pegou o garfo %d\n", i, esq);
    sleep(1);

    log_msg("Filosofo %d espera o garfo %d...\n", i, dir);
    pthread_mutex_lock(&garfo[dir]);   // deadlock acontece aqui

    log_msg("Filosofo %d comendo\n", i, -1);
    sleep(1);
    registrar_refeicao(i);

    pthread_mutex_unlock(&garfo[dir]);
    pthread_mutex_unlock(&garfo[esq]);
    return NULL;
}

int main() {
    pthread_t t[N];
    clock_gettime(CLOCK_MONOTONIC, &inicio_execucao);

    for (int i = 0; i < N; i++)
        pthread_mutex_init(&garfo[i], NULL);

    for (long long i = 0; i < N; i++)
        pthread_create(&t[i], NULL, filosofo, (void *)i);

    for (int i = 0; i < N; i++)
        pthread_join(t[i], NULL);

    imprimir_resumo();
    return 0;
}