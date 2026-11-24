#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#define N 5

pthread_mutex_t garfo[N];

void *filosofo(void *arg) {
    int i = (long long)arg;
    int esq = i;
    int dir = (i + 1) % N;

    pthread_mutex_lock(&garfo[esq]);
    printf("Filosofo %d pegou o garfo %d\n", i, esq);
    sleep(1);

    printf("Filosofo %d espera o garfo %d...\n", i, dir);
    pthread_mutex_lock(&garfo[dir]);   // deadlock acontece aqui

    printf("Filosofo %d comendo\n", i);
    sleep(1);

    pthread_mutex_unlock(&garfo[dir]);
    pthread_mutex_unlock(&garfo[esq]);
    return NULL;
}

int main() {
    pthread_t t[N];

    for (int i = 0; i < N; i++)
        pthread_mutex_init(&garfo[i], NULL);

    for (long long i = 0; i < N; i++)
        pthread_create(&t[i], NULL, filosofo, (void *)i);

    for (int i = 0; i < N; i++)
        pthread_join(t[i], NULL);

    return 0;
}