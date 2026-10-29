#include <pthread.h>
#include <stdio.h>
static void *run(void *p) { *(int *)p = 42; return NULL; }
int main(void) {
    pthread_t thread;
    int value = 0;
    if (pthread_create(&thread, NULL, run, &value) || pthread_join(thread, NULL) || value != 42) return 1;
    puts("JKOROS_GCC_PTHREAD_TEST_PASS");
    return 0;
}
