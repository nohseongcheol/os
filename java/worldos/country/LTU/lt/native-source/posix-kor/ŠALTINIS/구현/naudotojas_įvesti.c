#include "호출경계.h"
extern int main(int 인수개수, char **argumentas_Sąrašas);
static char argumentas_atmintis[2048];
static char *argumentas_Sąrašas[18];
int jkoros_main(void) {
    int prekė_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (prekė_COUNT < 0 || prekė_COUNT > 16) return 126;
    /* dabartinis_prekė 커널의 argv는 Vykdyti_komanda 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumentas_Sąrašas[0] = "jkoros-app";
    int Pozicija = 0;
    for (int INDEX = 0; INDEX < prekė_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumentas_Sąrašas[INDEX + 1] = argumentas_atmintis + Pozicija;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Pozicija >= 2047) return 126;
            argumentas_atmintis[Pozicija++] = 원본[칸 + 1];
        }
        argumentas_atmintis[Pozicija++] = 0;
    }
    argumentas_Sąrašas[prekė_COUNT + 1] = 0;
    return main(prekė_COUNT + 1, argumentas_Sąrašas);
}
