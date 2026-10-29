#include "hív_határ.h"
extern int main(int 인수개수, char **argumentum_Lista);
static char argumentum_Memória[2048];
static char *argumentum_Lista[18];
int jkoros_main(void) {
    int cikk_DARAB = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (cikk_DARAB < 0 || cikk_DARAB > 16) return 126;
    /* aktuális_cikk 커널의 argv는 végrehajt_parancs 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumentum_Lista[0] = "jkoros-app";
    int Pozíció = 0;
    for (int INDEX = 0; INDEX < cikk_DARAB; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumentum_Lista[INDEX + 1] = argumentum_Memória + Pozíció;
        for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 원본[0]; tárolóhely_bejegyzés++) {
            if (Pozíció >= 2047) return 126;
            argumentum_Memória[Pozíció++] = 원본[tárolóhely_bejegyzés + 1];
        }
        argumentum_Memória[Pozíció++] = 0;
    }
    argumentum_Lista[cikk_DARAB + 1] = 0;
    return main(cikk_DARAB + 1, argumentum_Lista);
}
